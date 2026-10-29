-- Student College ID Card Management System
-- PostgreSQL production schema. Run against a persistent managed database.
-- Do not use Vercel /tmp SQLite as durable production storage.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS admins (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name VARCHAR(160),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS students (
    id BIGSERIAL PRIMARY KEY,
    register_number VARCHAR(80) NOT NULL UNIQUE,
    student_name VARCHAR(200) NOT NULL,
    college_name VARCHAR(200) NOT NULL DEFAULT 'JOY UNIVERSITY',
    department VARCHAR(160) NOT NULL,
    course VARCHAR(160),
    academic_year VARCHAR(40),
    year_of_study VARCHAR(40),
    date_of_birth DATE,
    blood_group VARCHAR(8),
    phone VARCHAR(40),
    college_email VARCHAR(254),
    address TEXT,
    photo_object_key TEXT,
    validity_from DATE,
    validity_until DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_students_name ON students (LOWER(student_name));
CREATE INDEX IF NOT EXISTS idx_students_department ON students (department);
CREATE INDEX IF NOT EXISTS idx_students_academic_year ON students (academic_year);

CREATE TABLE IF NOT EXISTS card_templates (
    id BIGSERIAL PRIMARY KEY,
    template_name VARCHAR(120) NOT NULL,
    college_name VARCHAR(200) NOT NULL DEFAULT 'JOY UNIVERSITY',
    logo_object_key TEXT,
    primary_color VARCHAR(16) NOT NULL DEFAULT '#2057A8',
    secondary_color VARCHAR(16) NOT NULL DEFAULT '#FFFFFF',
    front_layout JSONB NOT NULL DEFAULT '{}'::jsonb,
    back_text TEXT,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS id_cards (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    template_id BIGINT REFERENCES card_templates(id) ON DELETE SET NULL,
    verification_token UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'deactivated', 'expired')),
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    generated_by BIGINT REFERENCES admins(id) ON DELETE SET NULL,
    pdf_object_key TEXT,
    UNIQUE (student_id, template_id)
);
CREATE INDEX IF NOT EXISTS idx_id_cards_status ON id_cards(status);
CREATE INDEX IF NOT EXISTS idx_id_cards_student ON id_cards(student_id);

CREATE TABLE IF NOT EXISTS imports (
    id BIGSERIAL PRIMARY KEY,
    original_filename TEXT NOT NULL,
    file_type VARCHAR(8) NOT NULL CHECK (file_type IN ('xlsx', 'csv')),
    status VARCHAR(20) NOT NULL DEFAULT 'preview' CHECK (status IN ('preview', 'completed', 'failed')),
    total_rows INTEGER NOT NULL DEFAULT 0,
    valid_rows INTEGER NOT NULL DEFAULT 0,
    imported_rows INTEGER NOT NULL DEFAULT 0,
    updated_rows INTEGER NOT NULL DEFAULT 0,
    skipped_rows INTEGER NOT NULL DEFAULT 0,
    created_by BIGINT REFERENCES admins(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS import_rows (
    id BIGSERIAL PRIMARY KEY,
    import_id BIGINT NOT NULL REFERENCES imports(id) ON DELETE CASCADE,
    source_row_number INTEGER NOT NULL,
    register_number VARCHAR(80),
    raw_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    normalized_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(20) NOT NULL CHECK (status IN ('valid', 'invalid', 'duplicate', 'imported', 'updated', 'skipped')),
    error_messages JSONB NOT NULL DEFAULT '[]'::jsonb,
    student_id BIGINT REFERENCES students(id) ON DELETE SET NULL,
    UNIQUE (import_id, source_row_number)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    admin_id BIGINT REFERENCES admins(id) ON DELETE SET NULL,
    action VARCHAR(80) NOT NULL,
    entity_type VARCHAR(80),
    entity_id VARCHAR(100),
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create the first administrator using the application's password-hashing helper.
-- Never store a plaintext password here.
