# Deployment Guide - UPI Fraud Detection System

## 📋 Table of Contents

1. [Production Checklist](#production-checklist)
2. [Backend Deployment](#backend-deployment)
3. [Frontend Deployment](#frontend-deployment)
4. [Database Setup](#database-setup)
5. [Security Configuration](#security-configuration)
6. [Performance Optimization](#performance-optimization)

---

## Production Checklist

### Before Deployment

- [ ] Set DEBUG=False in Django settings
- [ ] Configure proper SECRET_KEY
- [ ] Set up PostgreSQL database
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up CORS properly
- [ ] Configure static files serving
- [ ] Set up SSL/HTTPS
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Review security settings
- [ ] Test all endpoints
- [ ] Load test the application

---

## Backend Deployment

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**:

```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Heroku App**:

```bash
cd backend
heroku create upi-fraud-detection-api
```

3. **Add PostgreSQL**:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Configure Environment Variables**:

```bash
heroku config:set SECRET_KEY='your-secret-key-here'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='upi-fraud-detection-api.herokuapp.com'
heroku config:set CORS_ALLOWED_ORIGINS='https://your-frontend-url.vercel.app'
```

5. **Create Procfile**:

```bash
# backend/Procfile
web: gunicorn upi_fraud_detection.wsgi --log-file -
release: python manage.py migrate --run-syncdb
```

6. **Update requirements.txt**:

```bash
# Add these to requirements.txt
gunicorn==21.2.0
dj-database-url==2.1.0
whitenoise==6.6.0
```

7. **Update settings.py for Production**:

```python
# Add to settings.py
import dj_database_url

# Database
if not DEBUG:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

8. **Deploy**:

```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Option 2: Deploy to DigitalOcean

1. **Create Droplet**:

   - Ubuntu 22.04 LTS
   - Minimum 2GB RAM

2. **SSH into Droplet**:

```bash
ssh root@your-droplet-ip
```

3. **Install Dependencies**:

```bash
apt update
apt upgrade -y
apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

4. **Setup PostgreSQL**:

```bash
sudo -u postgres psql
CREATE DATABASE upi_fraud_db;
CREATE USER upi_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE upi_fraud_db TO upi_user;
\q
```

5. **Clone Repository**:

```bash
cd /var/www
git clone your-repo-url
cd upi-fraud-detection/backend
```

6. **Setup Python Environment**:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

7. **Configure Environment**:

```bash
nano .env
# Add production settings
```

8. **Run Migrations**:

```bash
python manage.py migrate --run-syncdb
python manage.py collectstatic
```

9. **Setup Gunicorn Service**:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/upi-fraud-detection/backend
ExecStart=/var/www/upi-fraud-detection/backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/upi-fraud-detection/backend/gunicorn.sock \
          upi_fraud_detection.wsgi:application

[Install]
WantedBy=multi-user.target
```

10. **Start Gunicorn**:

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

11. **Configure Nginx**:

```bash
sudo nano /etc/nginx/sites-available/upi-fraud-detection
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/upi-fraud-detection/backend;
    }

    location /media/ {
        root /var/www/upi-fraud-detection/backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/upi-fraud-detection/backend/gunicorn.sock;
    }
}
```

12. **Enable Nginx Site**:

```bash
sudo ln -s /etc/nginx/sites-available/upi-fraud-detection /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

13. **Setup SSL with Let's Encrypt**:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Frontend Deployment

### Option 1: Deploy to Vercel (Recommended)

1. **Install Vercel CLI**:

```bash
npm i -g vercel
```

2. **Login to Vercel**:

```bash
vercel login
```

3. **Deploy**:

```bash
cd frontend
vercel
```

4. **Configure Environment Variables**:

   - Go to Vercel Dashboard
   - Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL=https://your-backend-url.com`

5. **Deploy Production**:

```bash
vercel --prod
```

### Option 2: Deploy to Netlify

1. **Install Netlify CLI**:

```bash
npm install -g netlify-cli
```

2. **Build Project**:

```bash
cd frontend
npm run build
```

3. **Deploy**:

```bash
netlify deploy --prod
```

4. **Configure Environment**:
   - Go to Netlify Dashboard
   - Site settings → Build & deploy → Environment
   - Add: `NEXT_PUBLIC_API_URL`

---

## Database Setup

### PostgreSQL Production Setup

1. **Create Database**:

```sql
CREATE DATABASE upi_fraud_db;
CREATE USER upi_user WITH PASSWORD 'strong-password-here';
ALTER ROLE upi_user SET client_encoding TO 'utf8';
ALTER ROLE upi_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE upi_user SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE upi_fraud_db TO upi_user;
```

2. **Update Django Settings**:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'upi_fraud_db',
        'USER': 'upi_user',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Run Migrations**:

```bash
python manage.py migrate --run-syncdb
```

---

## Security Configuration

### Django Security Settings

```python
# settings.py

# Security
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://your-frontend-domain.com',
]
CORS_ALLOW_CREDENTIALS = True
```

### Environment Variables

Create `.env` file:

```env
SECRET_KEY=your-very-long-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://frontend-domain.com
```

---

## Performance Optimization

### Backend Optimization

1. **Database Indexing**:

```python
# Add to models.py
class Transaction(models.Model):
    # ... existing fields ...

    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_fraud']),
            models.Index(fields=['transaction_id']),
        ]
```

2. **Query Optimization**:

```python
# Use select_related and prefetch_related
transactions = Transaction.objects.select_related('user').all()
```

3. **Caching**:

```python
# Install Redis
pip install django-redis

# Add to settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

4. **Database Connection Pooling**:

```python
DATABASES = {
    'default': {
        # ... other settings ...
        'CONN_MAX_AGE': 600,
    }
}
```

### Frontend Optimization

1. **Image Optimization**:

```javascript
// Use Next.js Image component
import Image from "next/image";
```

2. **Code Splitting**: Already handled by Next.js

3. **Bundle Analysis**:

```bash
npm install @next/bundle-analyzer
```

4. **Enable Compression** in `next.config.js`:

```javascript
module.exports = {
  compress: true,
  // ... other settings
};
```

---

## Monitoring & Logging

### Backend Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Performance Monitoring

1. **Install Sentry**:

```bash
pip install sentry-sdk
```

2. **Configure Sentry**:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

---

## Backup Strategy

### Database Backup

```bash
# Create backup script
#!/bin/bash
pg_dump upi_fraud_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

### Media Files Backup

```bash
# Use rsync or cloud storage
rsync -av /var/www/upi-fraud-detection/backend/media/ /backup/media/
```

---

## Post-Deployment

1. **Test all endpoints**
2. **Monitor error logs**
3. **Check performance metrics**
4. **Set up uptime monitoring**
5. **Configure automated backups**
6. **Document any issues**
7. **Set up alerting**

---

## Troubleshooting

### Common Issues

1. **Static files not loading**:

```bash
python manage.py collectstatic
```

2. **Database connection errors**:

   - Check PostgreSQL is running
   - Verify credentials
   - Check firewall rules

3. **CORS errors**:

   - Verify CORS_ALLOWED_ORIGINS
   - Check frontend URL configuration

4. **502 Bad Gateway**:
   - Check Gunicorn is running
   - Verify Nginx configuration
   - Check socket permissions

---

## Support

For deployment issues:

1. Check logs: `/var/log/nginx/error.log`
2. Check Django logs
3. Review Gunicorn logs: `journalctl -u gunicorn`

---

**Remember**: Always test in a staging environment before deploying to production!
