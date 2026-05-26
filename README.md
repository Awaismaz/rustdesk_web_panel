# RustDesk Web Panel

A Django-based web control panel for [RustDesk](https://github.com/rustdesk/rustdesk) — the open-source remote desktop alternative to TeamViewer/AnyDesk. Lets you administer self-hosted RustDesk servers from a browser instead of the CLI.

## What it does

- Centralised admin UI for a self-hosted RustDesk deployment
- Web-based control panel (`control_panel/` app)
- Core Django wiring (`core/` app) handling routing, settings, and shared logic

## Stack

- Django (Python)
- SQLite (development; swap for Postgres in production)

## Quick start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/> and log in with the superuser credentials.

## Layout

```
rustdesk_web_panel/
├── control_panel/   # Admin UI app
├── core/            # Shared models, routing, settings
├── media/           # Uploaded files
├── staticfiles/     # Collected static assets
└── manage.py
```

## Status

Companion tool for the [RustDesk fork](https://github.com/Awaismaz/rustdesk). Self-hosting-focused.
