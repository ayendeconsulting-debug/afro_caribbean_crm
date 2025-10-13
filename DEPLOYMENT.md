# 🚀 Production Deployment Guide

Complete guide for deploying the Afro-Caribbean CRM system to production on AWS or other cloud providers.

## Pre-Deployment Checklist

### ✅ Security Configuration

- [ ] Generate a strong `SECRET_KEY` (use `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- [ ] Set `DEBUG = False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Enable HTTPS (`SECURE_SSL_REDIRECT = True`)
- [ ] Set secure cookie flags (`SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`)
- [ ] Review and adjust rate limiting
- [ ] Set up proper email backend (not console)
- [ ] Configure database backups
- [ ] Enable application monitoring/logging

### ✅ Environment Variables

Ensure all these are set in production `.env`:

```env
# Production Settings
DEBUG=False
SECRET_KEY=your-production-secret-key-very-long-and-random
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# SSL/HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Database (Use managed PostgreSQL)
DB_NAME=crm_production
DB_USER=crm_prod_user
DB_PASSWORD=very-strong-password
DB_HOST=your-rds-endpoint.amazonaws.com
DB_PORT=5432

# Email (Use SES or SendGrid)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-user
EMAIL_HOST_PASSWORD=your-ses-smtp-password

# Frontend
FRONTEND_URL=https://yourdomain.com

# Redis (for Celery)
REDIS_URL=redis://your-elasticache-endpoint:6379/0
```

---

## Option 1: AWS Deployment (Recommended)

### Architecture

```
┌─────────────────┐
│  Route 53 (DNS) │
└────────┬────────┘
         │
┌────────▼────────────┐
│  CloudFront (CDN)   │
│  + SSL Certificate  │
└────────┬────────────┘
         │
┌────────▼────────────┐
│  Application        │
│  Load Balancer      │
└────────┬────────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼──┐   ┌───▼──┐
│ ECS  │   │ ECS  │  (Auto-scaling)
│ Task │   │ Task │
└───┬──┘   └───┬──┘
    │          │
    └────┬─────┘
         │
┌────────▼────────────┐
│  RDS PostgreSQL     │
│  (Multi-AZ)         │
└─────────────────────┘
         │
┌────────▼────────────┐
│  ElastiCache Redis  │
└─────────────────────┘
         │
┌────────▼────────────┐
│  S3 (Static/Media)  │
└─────────────────────┘
```

### Step-by-Step AWS Deployment

#### 1. Database Setup (RDS)

```bash
# Create PostgreSQL database in RDS
# - Engine: PostgreSQL 15+
# - Instance class: db.t3.micro (start small)
# - Multi-AZ deployment: Yes (for production)
# - Storage: 20GB (can auto-scale)
# - Enable automated backups
```

#### 2. Redis Setup (ElastiCache)

```bash
# Create Redis cluster in ElastiCache
# - Engine: Redis 7.0+
# - Node type: cache.t3.micro (start small)
# - Number of replicas: 1-2
```

#### 3. S3 Buckets

```bash
# Create S3 buckets
aws s3 mb s3://afro-caribbean-crm-static
aws s3 mb s3://afro-caribbean-crm-media

# Set bucket policies for public read on static files
```

#### 4. ECS/Fargate Setup

**Create Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install production server
RUN pip install gunicorn

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD python manage.py migrate && \
    gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
```

**Build and Push to ECR:**

```bash
# Create ECR repository
aws ecr create-repository --repository-name afro-caribbean-crm

# Build and push Docker image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker build -t afro-caribbean-crm .
docker tag afro-caribbean-crm:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/afro-caribbean-crm:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/afro-caribbean-crm:latest
```

**Create ECS Task Definition:**

```json
{
  "family": "afro-caribbean-crm",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "django",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/afro-caribbean-crm:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DEBUG", "value": "False"}
      ],
      "secrets": [
        {"name": "SECRET_KEY", "valueFrom": "arn:aws:secretsmanager:..."},
        {"name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:..."}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/afro-caribbean-crm",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 5. Application Load Balancer

```bash
# Create ALB
# - Type: Application Load Balancer
# - Scheme: Internet-facing
# - Listeners: HTTP (80) and HTTPS (443)
# - Target group: ECS service
# - Health check: /api/customers/health/
```

#### 6. SSL Certificate (ACM)

```bash
# Request certificate in AWS Certificate Manager
aws acm request-certificate \
    --domain-name yourdomain.com \
    --subject-alternative-names www.yourdomain.com \
    --validation-method DNS
```

#### 7. Auto Scaling

```bash
# Configure ECS service auto-scaling
# - Min tasks: 2
# - Max tasks: 10
# - Target tracking: CPU utilization 70%
```

---

## Option 2: Traditional VPS Deployment (DigitalOcean, Linode, etc.)

### Requirements

- Ubuntu 22.04 LTS server
- At least 2GB RAM
- 20GB storage

### Step 1: Server Setup

```bash
# SSH into server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3.12 python3-pip python3-venv postgresql postgresql-contrib nginx redis-server

# Create application user
adduser crm
usermod -aG sudo crm
su - crm
```

### Step 2: PostgreSQL Setup

```bash
sudo -u postgres psql

CREATE DATABASE afro_caribbean_crm;
CREATE USER crm_user WITH PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE afro_caribbean_crm TO crm_user;
\q
```

### Step 3: Application Setup

```bash
# Clone/upload your code
cd /home/crm
mkdir app
cd app
# Upload your code here

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file with production settings
nano .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Step 4: Gunicorn Setup

**Create systemd service:**

```bash
sudo nano /etc/systemd/system/crm.service
```

```ini
[Unit]
Description=Afro-Caribbean CRM Gunicorn daemon
After=network.target

[Service]
User=crm
Group=www-data
WorkingDirectory=/home/crm/app
Environment="PATH=/home/crm/app/venv/bin"
ExecStart=/home/crm/app/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/crm/app/crm.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable service
sudo systemctl start crm
sudo systemctl enable crm
```

### Step 5: Nginx Setup

```bash
sudo nano /etc/nginx/sites-available/crm
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/crm/app/staticfiles/;
    }

    location /media/ {
        alias /home/crm/app/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/crm/app/crm.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/crm /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Step 7: Celery Setup (for notifications)

```bash
sudo nano /etc/systemd/system/celery.service
```

```ini
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=crm
Group=www-data
WorkingDirectory=/home/crm/app
Environment="PATH=/home/crm/app/venv/bin"
ExecStart=/home/crm/app/venv/bin/celery -A config worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start celery
sudo systemctl enable celery
```

---

## Monitoring & Maintenance

### Application Monitoring

1. **Sentry (Error Tracking)**
```bash
pip install sentry-sdk
```

Add to `settings.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=0.1,
)
```

2. **Prometheus + Grafana (Metrics)**
```bash
pip install django-prometheus
```

### Database Backups

**Automated PostgreSQL Backups:**

```bash
# Create backup script
nano /home/crm/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/crm/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U crm_user afro_caribbean_crm | gzip > $BACKUP_DIR/crm_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "crm_*.sql.gz" -mtime +30 -delete
```

```bash
chmod +x /home/crm/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /home/crm/backup.sh
```

### Log Rotation

```bash
sudo nano /etc/logrotate.d/crm
```

```
/home/crm/app/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 crm www-data
    sharedscripts
}
```

---

## Post-Deployment Testing

```bash
# Test health endpoint
curl https://yourdomain.com/api/customers/health/

# Test registration
curl -X POST https://yourdomain.com/api/customers/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#","password_confirm":"Test123!@#","first_name":"Test","last_name":"User"}'

# Check logs
tail -f /home/crm/app/logs/django.log
```

---

## Troubleshooting

### Issue: 502 Bad Gateway
**Solution:** Check Gunicorn is running: `sudo systemctl status crm`

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic` and check Nginx config

### Issue: Database connection errors
**Solution:** Check PostgreSQL is running and credentials are correct

### Issue: High memory usage
**Solution:** Reduce Gunicorn workers or upgrade server

---

## Scaling Considerations

- **Database**: Use read replicas for heavy read operations
- **Caching**: Implement Redis caching for frequently accessed data
- **CDN**: Use CloudFront or similar for static files
- **Auto-scaling**: Configure based on CPU/memory metrics
- **Load balancing**: Use multiple application servers

---

## Security Maintenance

- [ ] Regular security updates: `apt update && apt upgrade`
- [ ] Monitor failed login attempts
- [ ] Review access logs weekly
- [ ] Update dependencies monthly: `pip list --outdated`
- [ ] Rotate secrets quarterly
- [ ] Audit user permissions
- [ ] Test backup restoration quarterly

---

**Your application is now production-ready! 🎉**
