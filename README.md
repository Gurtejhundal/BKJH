# Bibi Kaulan Ji Hospital Website

Production-oriented Django website for Bibi Kaulan Ji Hospital. This is a public hospital website with admin-controlled content and appointment request tracking, not a hospital management system.

## Stack

- Python, Django, PostgreSQL
- Django Templates
- HTMX for targeted dashboard updates
- Alpine.js for the mobile menu
- Structured CSS design system
- Django Admin plus a custom appointment dashboard
- Hostinger VPS deployment with Gunicorn, Nginx, SSL

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The development settings use SQLite unless `DATABASE_URL` is provided.

On Windows, you can also use:

```bat
launch.bat
```

It creates `.venv` if missing, installs requirements, runs migrations, and starts `127.0.0.1:8000`.

## Important URLs

- Public site: `/`
- Django Admin: `/admin/`
- Appointment dashboard: `/dashboard/appointments/`
- Sitemap: `/sitemap.xml`
- Robots: `/robots.txt`

## Content Rules

Do not publish unverified claims. Emergency availability, ambulance availability, doctors, departments, OPD timings, phone numbers, and address must be approved by the client before launch.

Appointment submissions create a request only. They do not confirm an appointment automatically.

## Appointment Workflow

- Public form saves `AppointmentRequest` with `Pending` status.
- Staff/admin dashboard is protected at `/dashboard/appointments/`.
- Staff can filter by status, date, department, and search name/phone.
- Staff can update status and internal admin notes.
- Appointment data is not rendered in public templates.

## Production Notes

Use `.env.example` as the production environment reference. Required production settings:

- `SECRET_KEY` must be unique and private.
- `DEBUG=False`
- `ALLOWED_HOSTS` must contain the live domain.
- `CSRF_TRUSTED_ORIGINS` must contain HTTPS origins.
- `DATABASE_URL` should point to PostgreSQL.
- SSL must be enabled at Nginx/Hostinger.

Run before launch:

```bash
python manage.py check --deploy
python manage.py migrate
python manage.py collectstatic
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for Hostinger VPS setup, Gunicorn, Nginx, SSL, backups, and launch checks.

## Out of Scope for v1

- Patient login
- Medical records
- Lab reports
- Online payments
- SMS or WhatsApp API automation
- Doctor slot booking engine
- Queue token system
- Billing, pharmacy, inventory, or full HMS features
