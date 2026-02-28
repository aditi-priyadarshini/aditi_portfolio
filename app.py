import os
import bcrypt
import requests
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from functools import wraps

# ── APP SETUP ────────────────────────────────────────────────
_here = os.path.dirname(os.path.abspath(__file__))
_candidates = [
    os.path.join(_here, "templates"),
    os.path.join(_here, "..", "templates"),
    "/var/task/templates",
]
TEMPLATES_DIR = next((p for p in _candidates if os.path.isdir(p)), _candidates[0])
app = Flask(__name__, template_folder=TEMPLATES_DIR)

@app.errorhandler(Exception)
def handle_exception(e):
    from flask import Response
    import traceback
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": str(e)}), 500
    return Response(f"<pre>{traceback.format_exc()}</pre>", status=500, mimetype="text/html")

# ── ENV CONFIG ──────────────────────────────────────────────
SUPABASE_URL          = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY     = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_KEY  = os.getenv("SUPABASE_SERVICE_KEY", "")
CLOUDINARY_CLOUD      = os.getenv("CLOUDINARY_CLOUD", "")

sb_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ── AUTH DECORATOR ───────────────────────────────────────────
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing authorization token"}), 401
            token = auth_header.split(" ", 1)[1]
            user = sb_admin.auth.get_user(token)
            if not user or not user.user:
                return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": "Auth failed", "detail": str(e)}), 401
        return f(*args, **kwargs)
    return decorated

# ── PAGE ROUTES ──────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html",
        supabase_url=SUPABASE_URL,
        supabase_anon_key=SUPABASE_ANON_KEY)

@app.route("/admin")
def admin():
    return render_template("admin.html",
        supabase_url=SUPABASE_URL,
        supabase_anon_key=SUPABASE_ANON_KEY)


# ── FAVICON ─────────────────────────────────────────────────
@app.route("/favicon.ico")
def favicon():
    return "", 204

# ── API: CONTACT FORM (public) ───────────────────────────────
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()
    if not name or not email or not message:
        return jsonify({"success": False, "error": "All fields required"}), 400
    try:
        sb_admin.from_("messages").insert({
            "name": name, "email": email, "message": message
        }).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── API: UPLOAD IMAGE (auth required) ───────────────────────
@app.route("/api/upload-image", methods=["POST"])
@require_auth
def upload_image():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    file = request.files["file"]
    if not file.content_type.startswith("image/"):
        return jsonify({"success": False, "error": "Only images allowed"}), 400
    file.seek(0, 2)
    if file.tell() > 10 * 1024 * 1024:
        return jsonify({"success": False, "error": "Max 10MB"}), 400
    file.seek(0)
    if not CLOUDINARY_CLOUD:
        return jsonify({"success": False, "error": "Cloudinary not configured"}), 500
    try:
        resp = requests.post(
            f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD}/image/upload",
            data={"upload_preset": "pharmacy_portfolio", "folder": "pharmacy-portfolio"},
            files={"file": (file.filename or "image.jpg", file.stream, file.content_type)},
            timeout=30
        )
        result = resp.json()
        if "error" in result:
            return jsonify({"success": False, "error": result["error"]["message"]}), 500
        return jsonify({"success": True, "url": result["secure_url"]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── API: ADMIN CRUD ──────────────────────────────────────────
ALLOWED_TABLES = {"profile", "education", "experience", "skills", "certifications", "projects", "messages"}

@app.route("/api/admin/<table>", methods=["GET"])
@require_auth
def admin_list(table):
    if table not in ALLOWED_TABLES:
        return jsonify({"error": "Invalid table"}), 400
    try:
        if table == "profile":
            result = sb_admin.from_(table).select("*").execute()
        elif table == "messages":
            result = sb_admin.from_(table).select("*").order("created_at", desc=True).execute()
        else:
            result = sb_admin.from_(table).select("*").order("sort_order", desc=False).execute()
        return jsonify({"success": True, "data": result.data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/<table>", methods=["POST"])
@require_auth
def admin_create(table):
    if table not in ALLOWED_TABLES or table == "messages":
        return jsonify({"error": "Invalid table"}), 400
    try:
        data = request.get_json()
        result = sb_admin.from_(table).insert(data).execute()
        return jsonify({"success": True, "data": result.data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/<table>/<item_id>", methods=["PUT"])
@require_auth
def admin_update(table, item_id):
    if table not in ALLOWED_TABLES:
        return jsonify({"error": "Invalid table"}), 400
    try:
        data = request.get_json()
        data.pop("id", None)
        data.pop("created_at", None)
        data.pop("updated_at", None)
        result = sb_admin.from_(table).update(data).eq("id", item_id).execute()
        return jsonify({"success": True, "data": result.data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/admin/<table>/<item_id>", methods=["DELETE"])
@require_auth
def admin_delete(table, item_id):
    if table not in ALLOWED_TABLES or table == "profile":
        return jsonify({"error": "Invalid table"}), 400
    try:
        sb_admin.from_(table).delete().eq("id", item_id).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ── HEALTH CHECK ─────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "supabase": bool(SUPABASE_URL), "cloudinary": bool(CLOUDINARY_CLOUD)})

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
