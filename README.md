# ADITI.LAB

Pharmaceutical R&D and formulation science portfolio, implemented in the existing Flask/Supabase application.

## Run

Install `requirements.txt`, set `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY` and optionally `SUPABASE_BUCKET`, then run `python app.py`. The public portfolio is at `/`; the authenticated content editor remains at `/admin`.

## Data compatibility

Profile, skills, projects, experience, education and certifications still load from Supabase. Contact messages still use `/api/contact`. Authentication, CRUD and storage uploads remain in the existing backend. Skills display as category groups; legacy proficiency values remain in the database.

For extended research dossiers, run `migrations/001_research_dossiers.sql` in the Supabase SQL editor. This migration only adds nullable text fields and does not modify existing records. The admin editor checks for the extended schema before showing or submitting those fields. Existing title/description/tags/link projects work without the migration. Missing dossier details explicitly show as not documented. No experimental results or qualifications are generated.

The original `supabase_schema.sql` contains generic example data and is not a migration for an existing database. Do not rerun its sample inserts against a populated portfolio.

## Frontend

`templates/index.html`, `static/lab.css` and `static/lab.js` provide the public design. Native SVG, IntersectionObserver and requestAnimationFrame implement the conceptual lab, release curve, process progress, active navigation and restrained pointer response. Diagrams are explicitly illustrative. The ticker can be paused; reduced-motion preferences disable autonomous animation. Native dialog provides keyboard focus containment and Escape dismissal.

## Validation

Run `python -m unittest discover -s tests -v` after installing the application dependencies. These tests mock Supabase and check page/assets, contact storage, authentication gates, CRUD payloads, and optional schema compatibility.

Browser validation covered 320px, 375px, 768px, 1024px, 1440px and 812px landscape, dossier focus and Escape, mobile navigation, contact success, reduced motion, theme switching and admin login using isolated fixtures. Live Supabase credentials were not present; production data and storage were not modified.
