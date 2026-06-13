# Technical Architecture

## Architecture Type

Modern Monolith.

Backend, routing, templates, forms, database modeling, admin management, and deployment live in one unified Django codebase.

This is the correct approach for this project because:

- Small/solo developer project
- Admin-heavy content management
- Security matters
- Time-to-market matters
- Scope is dynamic but not massively distributed
- Hospital staff need reliability, not microservice complexity

## Stack

| Layer | Choice |
|---|---|
| Backend | Django |
| Language | Python |
| Database | PostgreSQL |
| Frontend | Django Templates |
| Interactivity | HTMX + Alpine.js |
| Admin | Django Admin + custom appointment dashboard |
| Cache/Queue | Redis optional later |
| Hosting | Hostinger VPS |
| Web server | Nginx |
| App server | Gunicorn |
| SSL | Let's Encrypt / Hostinger SSL setup |
| Static files | WhiteNoise or Nginx-served static |
| Media files | Local VPS storage initially |

## Why Django

Django gives:

- Fast development
- Built-in admin
- ORM
- Authentication
- CSRF protection
- Forms
- Secure defaults
- Mature deployment ecosystem

This project needs content/admin control more than a complex frontend SPA.

## Why PostgreSQL

PostgreSQL is reliable for structured data:

- Doctors
- Departments
- OPD timings
- Appointments
- Gallery metadata
- Notices

SQLite is acceptable for early local development but not recommended for final production.

## Why HTMX

Use HTMX only where it improves UX:

- Appointment status updates in dashboard
- Department/doctor filters
- OPD timing filter
- Form submission feedback if needed

Do not turn every component into HTMX. Keep it purposeful.

## Why Alpine.js

Use Alpine.js for small frontend interactions:

- Mobile menu
- Accordions
- Gallery lightbox controls
- FAQ toggles
- Form UI states

Do not add React/Vue for this project.

## Why Redis Is Optional

Redis can help with:

- Caching
- Background jobs
- Email queues
- Rate limiting

But v1 likely does not need it. Add Redis only if:

- Traffic grows
- Email/SMS queues are added
- Caching becomes necessary
- Appointment notification queue is implemented

Adding Redis too early is over-engineering.

## Recommended Project Structure

```text
hospital_site/
  manage.py
  requirements.txt
  .env.example
  README.md
  config/
    settings/
      base.py
      development.py
      production.py
    urls.py
    wsgi.py
    asgi.py
  apps/
    core/
    hospital/
    appointments/
    gallery/
    dashboard/
  templates/
    base.html
    partials/
    pages/
  static/
    css/
    js/
    images/
  media/
  docs/
```

## Environment Variables

Use `.env` for:

```text
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DATABASE_URL=
CSRF_TRUSTED_ORIGINS=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

Never commit real secrets.

## Settings Split

Use:

- base.py
- development.py
- production.py

Production must have:

```python
DEBUG = False
ALLOWED_HOSTS = ["domain.com", "www.domain.com"]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

## Public URL Structure

```text
/                         Home
/about/                   About
/departments/             Department listing
/departments/<slug>/      Department detail
/doctors/                 Doctors
/opd-timing/              OPD timing
/appointment/             Appointment request
/emergency/               Emergency
/ambulance/               Ambulance
/gallery/                 Gallery
/services/                Services
/facilities/              Facilities
/contact/                 Contact/location
/dashboard/appointments/  Custom admin appointment dashboard
```

## Template Rules

Use componentized templates:

```text
templates/
  base.html
  partials/
    header.html
    footer.html
    mobile_action_bar.html
    emergency_strip.html
    department_card.html
    doctor_card.html
    appointment_form.html
  pages/
    home.html
    about.html
    departments.html
    department_detail.html
    doctors.html
    opd_timing.html
    appointment.html
    gallery.html
    contact.html
```

## Form Security

- Use Django forms.
- CSRF token required.
- Validate phone numbers.
- Validate required fields.
- Add spam honeypot field if needed.
- Rate limiting optional later.

## File Upload Security

- Restrict uploaded files to images.
- Limit file size.
- Rename uploaded files safely.
- Store outside static directory.
- Serve media carefully.

## Performance Rules

- Optimize images.
- Lazy-load gallery images.
- Keep CSS/JS minimal.
- Avoid heavy animation libraries.
- Avoid frontend framework bloat.
- Cache static assets.

## Backup Rules

Minimum production backup plan:

- Database backup weekly or more often
- Media folder backup
- Keep `.env` copy safely offline
- Keep GitHub repo updated

## Senior Architecture Rule

The architecture must be boring, reliable, and understandable. That is the correct engineering choice here.
