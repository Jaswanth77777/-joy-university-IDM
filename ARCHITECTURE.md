# Architecture — Student College ID Card Management System

## Current deployment and migration plan

The existing repository is a Flask application deployed to Vercel. Keep this deployment compatible while replacing ephemeral storage with a persistent relational database and persistent object storage. The React/Express/MySQL stack in the brief is a suggestion, not a requirement; Flask can deliver the same workflow without an unnecessary rewrite.

### Logical components

- Web UI: responsive admin dashboard, student list/profile editor, import wizard, card generator, reports, settings.
- Application/API: Flask routes for authentication, student CRUD, import preview/commit, card generation, verification and exports.
- Relational database: PostgreSQL/MySQL in production; SQLite only for local development. Vercel /tmp is ephemeral and must not be treated as persistent storage.
- Object storage: student photographs and college logo stored outside the application filesystem; database stores object keys/URLs.
- Import workflow: parse CSV/XLSX, normalize headers, preview and validate rows, identify duplicate register numbers, then commit valid rows in a transaction.
- Card service: one card per student, QR code with opaque verification token, card status and generation timestamp.
- Export service: combined PDF, individual PDFs/ZIP, A4 print sheets and CSV/XLSX exports.
- Audit log: record admin actions, imports, updates, deletes, card generation and deactivation.

## Database schema

See schema.sql. Key rules:
- students.register_number is unique after normalization.
- Internal IDs are separate from register numbers.
- Card generation is tracked independently from student data.
- QR verification uses a random opaque token; public verification never returns address, DOB, phone or email.
- Imports and import rows are persisted so administrators can review success/failure counts.
- Admin passwords are salted hashes, never plaintext.

## Import workflow

1. Upload CSV/XLSX with size and extension checks.
2. Detect worksheet/header row and map recognized aliases.
3. Preview rows and report required-field errors, invalid dates and duplicate register numbers before writing.
4. Admin confirms import.
5. In a database transaction, save only selected valid records; invalid rows are not committed.
6. Show an import report and provide failed rows for download.
7. Generate cards only for valid saved students; card count must equal selected valid student count.

## ID card and privacy rules

- Use CR80 dimensions (85.60 × 53.98 mm) for printable output.
- Front: logo, college name, photo, name, register number, department, course, academic year and validity.
- Back: college contact and policy text configured by an admin.
- QR points to verification using a random token, not a sequential database ID.
- Public verification returns only name, college, register number, department and active/expired status.
- Deactivated/expired cards must not verify as active.

## Production deployment requirements

Set environment variables for SECRET_KEY, DATABASE_URL, and object-storage credentials. Configure a persistent managed PostgreSQL/MySQL database and object storage before real student data is used. Do not store production records in /tmp, and do not commit secrets or student data to GitHub.

## Suggested test gates

- Import 50 unique rows -> 50 student records and 50 cards.
- Re-import same register numbers -> no duplicate student rows.
- Missing name/register number -> invalid row reported and not saved.
- Duplicate register number in a file -> duplicate reported.
- Export cards -> output count matches selection.
- QR for active card -> limited public verification response.
- QR for deactivated/expired card -> inactive response.
