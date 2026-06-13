# Deployment — Hostinger VPS

## Hosting Decision

Use Hostinger VPS, not normal shared hosting, for Django + PostgreSQL.

Django apps run as persistent Python processes through WSGI/ASGI. A VPS gives control over Python, Gunicorn, Nginx, PostgreSQL, SSL, environment variables, and background services if needed.

## Recommended Minimum VPS

For a small hospital website:

- 1 vCPU minimum
- 2–4 GB RAM preferred
- 40–50 GB storage preferred
- Ubuntu LTS

If using image uploads heavily, storage/backups matter more.

## Production Components

```text
Domain -> Nginx -> Gunicorn -> Django -> PostgreSQL
                         |
                      Media files
                         |
                    Static files
```

Optional later:

```text
Django -> Redis -> Background jobs/cache
```

## Server Setup Outline

### 1. Update server

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install packages

```bash
sudo apt install python3 python3-pip python3-venv git nginx postgresql postgresql-contrib -y
```

### 3. Create project user

```bash
sudo adduser hospitalweb
sudo usermod -aG sudo hospitalweb
```

### 4. Clone repository

```bash
git clone <repo-url> hospital-site
cd hospital-site
```

### 5. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Configure PostgreSQL

Create database and user.

```sql
CREATE DATABASE hospital_db;
CREATE USER hospital_user WITH PASSWORD 'strong_password_here';
ALTER ROLE hospital_user SET client_encoding TO 'utf8';
ALTER ROLE hospital_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hospital_user SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
```

### 7. Configure environment

Create `.env`:

```text
SECRET_KEY=strong-secret-key
DEBUG=False
ALLOWED_HOSTS=domain.com,www.domain.com,server-ip
DATABASE_URL=postgres://hospital_user:password@localhost:5432/hospital_db
CSRF_TRUSTED_ORIGINS=https://domain.com,https://www.domain.com
```

### 8. Run Django commands

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### 9. Gunicorn service

Create systemd service:

```ini
[Unit]
Description=gunicorn daemon for hospital website
After=network.target

[Service]
User=hospitalweb
Group=www-data
WorkingDirectory=/home/hospitalweb/hospital-site
ExecStart=/home/hospitalweb/hospital-site/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Enable:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 10. Nginx config

```nginx
server {
    server_name domain.com www.domain.com;

    location /static/ {
        alias /home/hospitalweb/hospital-site/staticfiles/;
    }

    location /media/ {
        alias /home/hospitalweb/hospital-site/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 11. SSL

Use Certbot or Hostinger SSL setup.

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d domain.com -d www.domain.com
```

## Media Storage

V1:

- Store media on VPS.
- Backup media folder.

Later:

- Move gallery/media to S3, Cloudinary, or similar if needed.

## Backup Plan

Minimum:

- Weekly PostgreSQL dump
- Weekly media folder backup
- GitHub repository updated
- Keep `.env` safely stored outside repo

Example DB backup:

```bash
pg_dump hospital_db > backup_$(date +%F).sql
```

## Monitoring Basic

Check:

```bash
sudo systemctl status gunicorn
sudo nginx -t
sudo systemctl status nginx
journalctl -u gunicorn -n 100
```

## Crash Recovery

Gunicorn should be managed by systemd. If it crashes, systemd can restart it if configured.

Add to service if desired:

```ini
Restart=always
RestartSec=3
```

## Deployment Risks

- Shared hosting may not support proper Django deployment.
- Wrong DEBUG setting can expose sensitive data.
- No backups can destroy client trust.
- Wrong file permissions can break media uploads.
- Large uncompressed images can slow the site badly.

## Senior Deployment Rule

A live medical website must not be treated like a college project. Keep deployment boring, secure, backed up, and documented.
