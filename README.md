# JOY UNIVERSITY ID Card Management System

Flask student profile and square ID card management system.

## Local

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Vercel

This repository includes `vercel.json` and `api/index.py`.

Important: Vercel serverless storage is ephemeral. SQLite data written on Vercel is not a permanent database. For production student records, replace the SQLite layer with a hosted database such as Postgres/Turso and store uploaded photos in object storage.

The app is otherwise configured as a Vercel Python deployment.


## New login + campus background

The system now opens with the JOY UNIVERSITY loading screen and then requires login.

Default local/demo login:
- Username: `admin`
- Password: `joy123`

For deployment, set `JOY_ADMIN_USER`, `JOY_ADMIN_PASSWORD`, and `SECRET_KEY` as environment variables.

### Exact campus background image

The application expects the uploaded campus image at:

`static/joy_university_campus.png`

The exact uploaded image should be copied/uploaded there. It is used as the fixed background on the loading, login, dashboard, form, and ID-card pages.

All authenticated pages include a **← Back** button and a **Logout** button.
