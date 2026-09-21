# Protekt Ze Brand (PZB)

PZB is a Flask-powered brand and community website built around reputation,
integrity, respect, purpose, and legacy.

## What changed

The project now uses Python + Flask instead of being deployed as static HTML.
That gives PZB clean routes and a foundation for accounts, forms, a database,
and an interactive archive later.

## Main routes

- `/` — Home
- `/about` — Origin story
- `/mission` — Mission and four pillars
- `/timeline` — Animated PZB timeline
- `/archive` — Community and real-moments archive
- `/badge` — PZB Badge of Vow

## Project structure

```text
pzb/
├── app.py                 # Flask routes and application entry point
├── requirements.txt       # Python packages for local use and Render
├── render.yaml            # Render deployment configuration
├── templates/             # Flask-rendered pages
├── assets/                # Shared CSS and JavaScript
├── founder/               # Existing founder profile pages
└── founders/
```

## Run locally (Linux / ChromeOS)

You need Python 3 installed. Check it with:

```bash
python3 --version
```

Create and activate an isolated project environment:

```bash
cd /home/nathanshako10/pzb
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the app:

```bash
python app.py
```

Open this in your browser:

```text
http://127.0.0.1:5000
```

Stop the server with `Ctrl + C`.

## Deploy on Render

1. Push this project to GitHub.
2. In Render, choose **New → Blueprint** and select the repository.
3. Render reads `render.yaml`, installs the packages, and starts `gunicorn app:app`.
4. Add your custom domain in the Render service settings after the first deploy.

## Future backend features

The Flask routes are deliberately simple today. Good next additions are a real
contact form, an Archive database, account-backed badges, and an admin page
for publishing PZB moments.
