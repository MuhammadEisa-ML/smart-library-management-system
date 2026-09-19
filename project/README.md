# ShelfWise — Smart Library Management System

A CS50-friendly Flask web application for library members and librarians.

## Features

- Member registration and secure password-hash login
- Admin/librarian login and access control
- Search by title, author, ISBN, or category, plus availability filters
- Borrow books for 14 days; return them with automatic Rs. 20/day overdue fines
- Favorites and a borrowing-history page
- Admin book creation, editing, deletion (when no loan history exists), active-loan view, and statistics
- Lightweight book recommendations based on matching categories
- SQLite database, automatically created and seeded with five books

## Install and run locally (Windows PowerShell)

From this `project` directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py app.py
```

Open `http://127.0.0.1:5000` in your browser. To stop the app, press `Ctrl+C` in PowerShell.

If PowerShell blocks activation, run this once in that PowerShell window, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Demo librarian account

| Field | Value |
| --- | --- |
| Email | `admin@library.local` |
| Password | `admin123` |

Change this account and set `FLASK_SECRET_KEY` before public deployment. The `library.db` file contains all local data; delete it only when you intentionally want a fresh database.

## Project structure

- `app.py` — Flask routes, business rules, schema, and seed data
- `templates/` — Jinja HTML pages
- `static/styles.css` — responsive visual design
- `requirements.txt` — the only required Python dependency

## Render deployment note

Use the build command `pip install -r requirements.txt` and start command `gunicorn app:app`. Render's local disk is ephemeral, so use a hosted PostgreSQL database for real persistent data.
