# JOY UNIVERSITY ID Card Management System

A Flask-based student profile manager with square, flip-front/back ID cards.

## Features

- JOY UNIVERSITY loading screen and login
- Student add, edit, search and delete
- Bulk CSV import with duplicate PRNs skipped
- Downloadable CSV import template
- Student photo upload
- Square 1:1 3D flip ID card with print support
- Five card themes: Jet Black (#0A0A0A), Cerulean Blue (#007BA7), Neon Rose (#FF2D95), Emerald, and Violet
- Theme selection remembered in the browser
- Responsive layout, Back button and Logout
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

## Bulk import CSV

Sign in, choose **Bulk Import**, and upload a CSV. The required headers are `name` and `prn`; optional headers are:

`department, course, year, batch, phone, email, blood_group, dob, hostel, address, photo`

Use the in-app **Download CSV Template** link to get an example file. Existing PRNs and rows missing name/PRN are skipped and counted in the result.

## Vercel deployment

The repository includes `vercel.json` and `api/index.py`.

**Persistence warning:** Vercel serverless filesystem storage is ephemeral. The SQLite database at `/tmp/joy_university.db` and photos stored as data URLs are not a durable production storage strategy. For real student records, use a hosted database such as Postgres/Turso and object storage for photos.

The campus background currently uses the JOY University website image URL:
https://joyuniversity.edu.in/images/JU_Header-Images-About-us.jpeg

This is a hosted reference image and may differ from the exact uploaded campus image.
