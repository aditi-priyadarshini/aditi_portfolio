-- ============================================================
-- PHARMACY PORTFOLIO — SUPABASE SCHEMA
-- Run this in Supabase SQL Editor (Dashboard → SQL Editor → New query)
-- ============================================================

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- ── PROFILE ─────────────────────────────────────────────────
create table if not exists profile (
  id            uuid primary key default uuid_generate_v4(),
  name          text not null default 'Your Name',
  tagline       text default 'Student Pharmacist',
  bio           text default 'Write your bio here...',
  photo_url     text,
  email         text,
  linkedin      text,
  github        text,
  university    text,
  year          text,
  gpa           text,
  phone         text,
  location      text,
  updated_at    timestamptz default now()
);

-- Insert default row
insert into profile (name, tagline, bio, university, year)
values ('Your Name', 'Student Pharmacist | Future Clinical Expert', 'Passionate pharmacy student dedicated to patient care and pharmaceutical sciences.', 'Your University', '4th Year')
on conflict do nothing;

-- ── EDUCATION ───────────────────────────────────────────────
create table if not exists education (
  id            uuid primary key default uuid_generate_v4(),
  institution   text not null,
  degree        text not null,
  field         text,
  start_date    text,
  end_date      text,
  description   text,
  achievements  text,
  is_current    boolean default false,
  sort_order    int default 0,
  created_at    timestamptz default now()
);

-- ── EXPERIENCE ──────────────────────────────────────────────
create table if not exists experience (
  id            uuid primary key default uuid_generate_v4(),
  title         text not null,
  organization  text not null,
  type          text default 'internship',  -- internship | rotation | community | research
  start_date    text,
  end_date      text,
  description   text,
  is_current    boolean default false,
  sort_order    int default 0,
  created_at    timestamptz default now()
);

-- ── SKILLS ──────────────────────────────────────────────────
create table if not exists skills (
  id            uuid primary key default uuid_generate_v4(),
  name          text not null,
  category      text default 'Clinical',  -- Clinical | Pharmaceutical | Soft | Tools
  proficiency   int default 80,           -- 0–100
  sort_order    int default 0,
  created_at    timestamptz default now()
);

-- ── CERTIFICATIONS ──────────────────────────────────────────
create table if not exists certifications (
  id              uuid primary key default uuid_generate_v4(),
  name            text not null,
  issuing_body    text,
  issue_date      text,
  expiry_date     text,
  credential_url  text,
  badge_url       text,
  sort_order      int default 0,
  created_at      timestamptz default now()
);

-- ── PROJECTS ────────────────────────────────────────────────
create table if not exists projects (
  id            uuid primary key default uuid_generate_v4(),
  title         text not null,
  description   text,
  tags          text,   -- comma-separated: "pharmacology,patient care"
  link          text,
  is_featured   boolean default false,
  sort_order    int default 0,
  created_at    timestamptz default now()
);

-- ── MESSAGES (contact form) ──────────────────────────────────
create table if not exists messages (
  id         uuid primary key default uuid_generate_v4(),
  name       text,
  email      text,
  message    text,
  is_read    boolean default false,
  created_at timestamptz default now()
);

-- ── ROW LEVEL SECURITY ───────────────────────────────────────
-- Public can read everything except messages
alter table profile        enable row level security;
alter table education      enable row level security;
alter table experience     enable row level security;
alter table skills         enable row level security;
alter table certifications enable row level security;
alter table projects       enable row level security;
alter table messages       enable row level security;

-- Public read policies
create policy "public_read_profile"        on profile        for select using (true);
create policy "public_read_education"      on education      for select using (true);
create policy "public_read_experience"     on experience     for select using (true);
create policy "public_read_skills"         on skills         for select using (true);
create policy "public_read_certifications" on certifications for select using (true);
create policy "public_read_projects"       on projects       for select using (true);

-- Public can insert messages (contact form)
create policy "public_insert_messages" on messages for insert with check (true);

-- Authenticated (admin) can do everything
create policy "admin_all_profile"        on profile        for all using (auth.role() = 'authenticated');
create policy "admin_all_education"      on education      for all using (auth.role() = 'authenticated');
create policy "admin_all_experience"     on experience     for all using (auth.role() = 'authenticated');
create policy "admin_all_skills"         on skills         for all using (auth.role() = 'authenticated');
create policy "admin_all_certifications" on certifications for all using (auth.role() = 'authenticated');
create policy "admin_all_projects"       on projects       for all using (auth.role() = 'authenticated');
create policy "admin_all_messages"       on messages       for all using (auth.role() = 'authenticated');

-- ── SAMPLE DATA ──────────────────────────────────────────────
insert into skills (name, category, proficiency, sort_order) values
  ('Clinical Pharmacology', 'Clinical', 90, 1),
  ('Patient Counseling', 'Clinical', 85, 2),
  ('Drug Interaction Analysis', 'Clinical', 80, 3),
  ('Compounding', 'Pharmaceutical', 75, 4),
  ('Pharmacokinetics', 'Pharmaceutical', 85, 5),
  ('Drug Dispensing', 'Pharmaceutical', 90, 6),
  ('Communication', 'Soft', 95, 7),
  ('Team Collaboration', 'Soft', 90, 8),
  ('Microsoft Office', 'Tools', 85, 9),
  ('Lexicomp / Micromedex', 'Tools', 80, 10);

insert into education (institution, degree, field, start_date, end_date, description, is_current, sort_order) values
  ('Your University', 'Doctor of Pharmacy (Pharm.D)', 'Pharmacy', '2021', 'Present', 'Pursuing a comprehensive pharmacy degree with focus on clinical practice and patient care.', true, 1);

insert into experience (title, organization, type, start_date, end_date, description, sort_order) values
  ('Clinical Rotation Intern', 'City General Hospital', 'rotation', 'Jun 2023', 'Aug 2023', 'Completed 500+ hours of clinical rotations across internal medicine, cardiology, and oncology departments.', 1),
  ('Community Pharmacy Intern', 'Health Plus Pharmacy', 'community', 'Jan 2023', 'May 2023', 'Assisted pharmacists in dispensing, patient counseling, and inventory management.', 2);

insert into certifications (name, issuing_body, issue_date, sort_order) values
  ('Basic Life Support (BLS)', 'American Heart Association', '2023', 1),
  ('Immunization Certificate', 'American Pharmacists Association', '2023', 2);

insert into projects (title, description, tags, is_featured, sort_order) values
  ('Medication Adherence Study', 'Research project analyzing factors affecting medication adherence in elderly patients with chronic conditions.', 'research,patient care,pharmacology', true, 1),
  ('Drug Interaction Checker', 'Developed a reference guide for common drug-drug interactions encountered in community pharmacy settings.', 'drug interactions,tools,pharmaceutical', false, 2);
