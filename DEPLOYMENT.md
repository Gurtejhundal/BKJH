# Hostinger VPS Deployment

This project is prepared for a Hostinger VPS running Ubuntu LTS, PostgreSQL, Gunicorn, Nginx, and SSL. Do not deploy with `DEBUG=True`.

## 1. Server Update

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git nginx postgresql postgresql-contrib certbot python3-certbot-nginx -y
```

## 2. Project User

```bash
sudo adduser hospitalweb
sudo usermod -aG sudo hospitalweb
su - hospitalweb
```

## 3. Clone Project

```bash
git clone https://github.com/Gurtejhundal/BKJH.git hospital-site
cd hospital-site
```

## 4. Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE hospital_db;
CREATE USER hospital_user WITH PASSWORD 'replace_with_strong_password';
ALTER ROLE hospital_user SET client_encoding TO 'utf8';
ALTER ROLE hospital_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE hospital_user SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
\q
```

## 6. Environment

Create `.env` from `.env.example` and set real values:

```bash
cp .env.example .env
nano .env
```

Required:

```text
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=domain.com,www.domain.com,server-ip
CSRF_TRUSTED_ORIGINS=https://domain.com,https://www.domain.com
DATABASE_URL=postgres://hospital_user:password@localhost:5432/hospital_db
SITE_URL=https://domain.com
```

Do not commit `.env`.

## 7. Django Commands

```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py check --deploy
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 8. Gunicorn Test

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```

Stop with `Ctrl+C` after confirming it starts.

## 9. Systemd

Copy `deploy/gunicorn.service.example` to:

```bash
sudo nano /etc/systemd/system/bkjh-gunicorn.service
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable bkjh-gunicorn
sudo systemctl start bkjh-gunicorn
sudo systemctl status bkjh-gunicorn
```

## 10. Nginx

Copy `deploy/nginx.conf.example` to:

```bash
sudo nano /etc/nginx/sites-available/bkjh
sudo ln -s /etc/nginx/sites-available/bkjh /etc/nginx/sites-enabled/bkjh
sudo nginx -t
sudo systemctl reload nginx
```

## 11. SSL

```bash
sudo certbot --nginx -d domain.com -d www.domain.com
```

After SSL is active, confirm:

```bash
python manage.py check --deploy
```

HSTS subdomain/preload should be enabled only after confirming all subdomains must use HTTPS.

## 12. Media Permissions

```bash
sudo chown -R hospitalweb:www-data /home/hospitalweb/hospital-site/media
sudo chmod -R 775 /home/hospitalweb/hospital-site/media
```

## 13. Backup Plan

Database:

```bash
pg_dump hospital_db > backup_$(date +%F).sql
```

Media:

```bash
tar -czf media_backup_$(date +%F).tar.gz media/
```

Keep database backups, media backups, and `.env` backups outside the public web root.

## 14. Restart Commands

```bash
sudo systemctl restart bkjh-gunicorn
sudo systemctl reload nginx
journalctl -u bkjh-gunicorn -n 100
```

## 15. Launch Checklist

- `DEBUG=False`
- Real `SECRET_KEY`
- Correct `ALLOWED_HOSTS`
- Correct `CSRF_TRUSTED_ORIGINS`
- HTTPS working
- `/admin/` login works
- `/dashboard/appointments/` requires staff login
- Appointment form creates pending request only
- Emergency number, ambulance number, address, and map verified by client
- `/robots.txt` works
- `/sitemap.xml` works
- Static files load
- Media upload works
- First database and media backup created
