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
