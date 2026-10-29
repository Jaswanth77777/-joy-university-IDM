# JOY UNIVERSITY ID Card Management System

Flask-based management for separate student and teacher/faculty profiles with square front/back ID cards.

## Features

- Student profiles: add, edit, search, delete and photo upload
- Separate teacher/faculty profiles and faculty ID cards
- Square 1:1 front/back cards, card colour themes and print support
- Student bulk import from CSV or Excel (.xlsx)
- Batch photo matching from ZIP or multiple image uploads
- Excel workbooks with photos embedded beside student rows are supported
- Bulk import supports batches larger than 100 rows, with front and back card previews for every imported student
- Required student fields: full name, PRN, phone number, branch/department, batch number, full address and photo
- JOY UNIVERSITY loading screen, login, responsive UI, Back button and Logout

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

Demo login:
- Username: `admin`
- Password: `joy123`

Set `JOY_ADMIN_USER`, `JOY_ADMIN_PASSWORD`, and `SECRET_KEY` environment variables before deployment.

## Bulk import students (50, 100, 500 or more rows)

1. Sign in and open **Bulk Import 100 IDs**.
2. Download the CSV or Excel template.
3. Fill in one student per row. Required columns: `name, prn, phone, department, batch, address, photo`. Optional columns include `course, year, email, blood_group, dob, hostel`.
4. Upload the CSV or Excel file and provide photos using one of these methods:
   - **Photo ZIP:** name each image to match the `photo` cell, e.g. `JU2026001.jpg`. If no photo names are supplied, the ZIP images are paired to rows in alphabetical filename order.
   - **Multiple images:** select images in the same order as spreadsheet rows.
   - **Embedded Excel photos:** place each student's image on that student's row in the worksheet. Keep the row order aligned.
5. Select **Import & Create ID Cards**. Every non-empty row is processed; missing name/PRN and save errors are reported. Existing PRNs are updated instead of duplicated. Photos can be added later from each student profile.
6. Select **Open ID Cards**, then **Print All Cards** to print the complete batch. The batch output includes a front and a back card for every imported student.

The importer accepts up to 100 rows per batch. For best results, keep each photo under 1 MB and use JPG or PNG images.

## Faculty ID cards

Open **Teachers**, add faculty with an employee ID, designation, department and photo, then open **Faculty ID** to preview and print the separate card. Student and faculty profiles are stored in separate tables.

## Vercel deployment note

The repository includes `vercel.json` and `api/index.py`. Vercel serverless request and filesystem limits can prevent large batches of photos from working reliably, and the SQLite database at `/tmp/joy_university.db` is ephemeral. For production batches and persistent student records, use hosted database and object storage and upload photos directly to that storage.


## Important deployment note

The current web app is still Flask + SQLite to preserve the existing Vercel deployment; it is not yet a React/Express/MySQL rewrite. Vercel's `/tmp` SQLite database is ephemeral and must not be used as the permanent store for real college records. Configure a persistent database and durable object storage before production use. `ARCHITECTURE.md` and `schema.sql` document the recommended production design.
