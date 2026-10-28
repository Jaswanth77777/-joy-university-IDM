# JOY UNIVERSITY ID Card Management System

Flask-based management for separate student and teacher/faculty profiles with square front/back 3D ID cards.

## Features

- JOY UNIVERSITY loading screen and login
- Student profiles: add, edit, search, delete and photo upload
- Faculty profiles in a separate database table and dashboard
- Separate student and faculty ID card designs
- Square 1:1 front/back cards with 3D flip and print support
- Quick colour choices: Jet Black (#0A0A0A), Cerulean Blue (#007BA7), Neon Rose (#FF2D95), Emerald and Violet
- Student bulk CSV import and downloadable CSV template
- Responsive UI, Back button and Logout
- SQLite for local development

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

## Bulk import students

Sign in and select **Bulk Import**. Required CSV headers: `name`, `prn`. Optional headers: `department, course, year, batch, phone, email, blood_group, dob, hostel, address, photo`. Existing PRNs and invalid rows are skipped and counted.

## Faculty ID cards

Open **Teachers** in the navigation, add faculty with an employee ID, designation, department and photo, then open **Faculty ID** to preview and print the separate card. Student and faculty profiles are stored in separate tables.

## Vercel deployment

The repository includes `vercel.json` and `api/index.py`.

**Persistence warning:** Vercel serverless filesystem storage is ephemeral. The SQLite database at `/tmp/joy_university.db` and photos stored as data URLs are not durable production storage. Use a hosted database (such as Postgres/Turso) and object storage for real records and photos.

The campus background currently uses:
https://joyuniversity.edu.in/images/JU_Header-Images-About-us.jpeg

This hosted campus image may differ from the exact image originally uploaded.
