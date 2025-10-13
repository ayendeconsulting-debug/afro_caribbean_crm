# 🚀 Quick Start Guide - Afro-Caribbean CRM

## Fastest Way to Get Started (5 minutes)

### Option 1: SQLite (No PostgreSQL needed - for quick testing)

1. **Modify settings.py** - Comment out PostgreSQL, use SQLite:
```python
# In config/settings.py, replace DATABASES with:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

2. **Run these commands:**
```bash
cd afro_caribbean_crm
source venv/bin/activate  # Already created
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

3. **Test the API:**
Visit: http://localhost:8000/api/docs/

### Option 2: Full PostgreSQL Setup (Recommended)

1. **Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
brew services start postgresql

# Windows
# Download from: https://www.postgresql.org/download/windows/
```

2. **Create Database:**
```bash
sudo -u postgres psql
CREATE DATABASE afro_caribbean_crm;
CREATE USER crm_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE afro_caribbean_crm TO crm_user;
\q
```

3. **Update .env file** with your database credentials

4. **Run migrations:**
```bash
cd afro_caribbean_crm
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
mkdir logs
python manage.py runserver
```

## 🧪 Test Your Setup

### 1. Health Check
```bash
curl http://localhost:8000/api/customers/health/
```

Expected: `{"status": "healthy", "message": "Afro-Caribbean CRM API is running"}`

### 2. Register a Test Customer
```bash
curl -X POST http://localhost:8000/api/customers/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#",
    "password_confirm": "Test123!@#",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/customers/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#"
  }'
```

Save the `access` token from the response!

### 4. Get Profile
```bash
curl http://localhost:8000/api/customers/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## 📱 Access Points

- **API Documentation**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/
- **API Health Check**: http://localhost:8000/api/customers/health/

## 🎯 What You've Built (Phase 1 Complete!)

✅ Secure customer registration with email verification
✅ JWT-based authentication
✅ Customer profile management  
✅ Admin dashboard for business owner
✅ Rate limiting on sensitive endpoints
✅ Password hashing with Argon2
✅ Complete API documentation
✅ Database models for customer data
✅ Notification preference management
✅ Customer notes system for business owner

## 🔜 Next Steps

You now have a solid foundation! Ready for:
- Phase 2: Customer Dashboard UI
- Phase 3: Enhanced Admin Features  
- Phase 4: Promotion System
- Phase 5: Notification Infrastructure
- Phase 6: Mobile Apps

## 🆘 Quick Troubleshooting

**Port 8000 already in use?**
```bash
python manage.py runserver 8080
```

**Can't connect to database?**
- Check PostgreSQL is running: `sudo service postgresql status`
- Verify credentials in `.env` file

**Import errors?**
```bash
pip install -r requirements.txt
```

**Need to reset everything?**
```bash
python manage.py flush
python manage.py createsuperuser
```

## 💡 Pro Tips

1. Use the Swagger UI at `/api/docs/` for interactive API testing
2. Check the console for email verification links (in development mode)
3. Admin panel is at `/admin/` - use your superuser credentials
4. All passwords must have: 8+ chars, letters, numbers, special chars
5. JWT access tokens expire in 1 hour, refresh tokens in 24 hours

Happy coding! 🎉
