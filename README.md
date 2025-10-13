# Afro-Caribbean CRM System - Phase 1

A secure, scalable Customer Relationship Management system for an African and Caribbean food retail store.

## 🎯 Project Overview

This is **Phase 1** of a multi-phase CRM system that includes:
- ✅ Secure customer registration and authentication
- ✅ JWT-based API authentication
- ✅ Customer profile management
- ✅ Email verification system
- ✅ Admin dashboard for business owner
- ✅ Customer database management
- ✅ Rate limiting and security features
- ✅ Comprehensive API documentation

## 🏗️ Technology Stack

- **Backend**: Django 5.0.1 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Argon2 (most secure)
- **API Documentation**: DRF Spectacular (Swagger/OpenAPI)
- **Task Queue**: Celery + Redis (for future notifications)

## 🔒 Security Features

1. **Password Security**
   - Argon2 password hashing
   - Strong password validation (min 8 chars, letters, numbers, special chars)
   - Password change functionality

2. **Authentication**
   - JWT-based authentication
   - Token refresh mechanism
   - Rate limiting on login (10/hour) and registration (5/hour)

3. **Email Verification**
   - Secure token-based email verification
   - 24-hour token expiry
   - Verification required for notifications

4. **Security Headers**
   - XSS protection
   - CSRF protection
   - Clickjacking protection
   - Content type sniffing protection

5. **Rate Limiting**
   - Anonymous: 100 requests/hour
   - Authenticated: 1000 requests/hour
   - Custom limits for sensitive endpoints

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Redis (for future Celery tasks)
- pip and virtualenv

## 🚀 Setup Instructions

### 1. Clone and Setup Virtual Environment

```bash
cd afro_caribbean_crm
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-generate-a-strong-one
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=afro_caribbean_crm
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Setup PostgreSQL Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE afro_caribbean_crm;

# Create user (optional)
CREATE USER crm_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE afro_caribbean_crm TO crm_user;

# Exit PostgreSQL
\q
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Business Owner)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Create logs directory

```bash
mkdir logs
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔗 API Endpoints

### Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/customers/register/` | Register a new customer |
| POST | `/api/customers/login/` | Login and get JWT tokens |
| POST | `/api/customers/verify-email/` | Verify email address |
| POST | `/api/customers/token/refresh/` | Refresh access token |
| GET | `/api/customers/health/` | Health check |

### Customer Endpoints (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers/profile/` | Get current user profile |
| PUT/PATCH | `/api/customers/profile/` | Update user profile |
| GET | `/api/customers/dashboard/` | Get dashboard data |
| POST | `/api/customers/change-password/` | Change password |

### Admin Endpoints (Staff Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers/admin/customers/` | List all customers |
| GET | `/api/customers/admin/customers/{id}/` | Get specific customer |
| GET/POST | `/api/customers/admin/customers/{id}/notes/` | Manage customer notes |

## 🧪 Testing the API

### 1. Register a New Customer

```bash
curl -X POST http://localhost:8000/api/customers/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+15551234567"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/customers/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "SecurePass123!"
  }'
```

Save the returned `access` token for authenticated requests.

### 3. Get Profile (Authenticated)

```bash
curl -X GET http://localhost:8000/api/customers/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Update Profile

```bash
curl -X PATCH http://localhost:8000/api/customers/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+15559876543",
    "city": "Toronto",
    "dietary_preferences": "Vegetarian"
  }'
```

## 📊 Database Models

### Customer Model

**Fields:**
- `id` (UUID): Unique identifier
- `email` (Email): Login credential
- `first_name`, `last_name`: Personal info
- `phone_number`: For SMS notifications
- `street_address`, `city`, `province_state`, `postal_code`, `country`: Address
- `dietary_preferences`, `favorite_products`: Customer preferences
- `email_notifications`, `sms_notifications`, `push_notifications`: Notification preferences
- `is_active`, `is_verified`, `is_staff`: Account status
- `total_purchases`, `loyalty_points`: Customer metrics
- `date_joined`, `last_login`, `updated_at`: Timestamps

### CustomerNote Model

For business owner to keep notes about customers:
- `id` (UUID): Unique identifier
- `customer`: Foreign key to Customer
- `note`: Text content
- `created_by`: Staff member who created the note
- `created_at`, `updated_at`: Timestamps

## 🔐 Authentication Flow

1. **Registration**
   - Customer registers with email and password
   - System sends verification email
   - Customer receives JWT tokens immediately

2. **Email Verification**
   - Customer clicks verification link from email
   - Token is validated and account is verified
   - Customer can now receive notifications

3. **Login**
   - Customer logs in with email and password
   - System returns access token (valid for 1 hour) and refresh token (valid for 24 hours)

4. **Token Refresh**
   - When access token expires, use refresh token to get a new access token
   - No need to login again

## 🎨 Admin Interface

Access the Django admin at: `http://localhost:8000/admin/`

**Features:**
- View and manage all customers
- Add notes to customer profiles
- Filter customers by status, verification, date joined
- Search by email, name, phone number
- View customer metrics (purchases, loyalty points)

## 🔄 Next Steps (Phase 2-6)

### Phase 2: Customer Dashboard & Profile (Weeks 3-4)
- Enhanced dashboard UI
- Profile picture upload
- Preference management

### Phase 3: Admin Panel & Customer Management (Weeks 5-6)
- Advanced customer search and filtering
- Analytics dashboard
- Export customer data

### Phase 4: Promotion System (Weeks 7-8)
- Create and schedule promotions
- Customer segmentation
- Promotion templates

### Phase 5: Notification Infrastructure (Weeks 9-10)
- Email campaigns
- SMS integration
- Push notification setup

### Phase 6: Mobile Apps (Weeks 11-14)
- React Native apps
- App store submission

## 🐛 Common Issues

### Issue: Database connection error
**Solution**: Check PostgreSQL is running and credentials in `.env` are correct

### Issue: Email not sending
**Solution**: In development, emails print to console. Check your terminal output.

### Issue: Migration errors
**Solution**: Delete migrations and database, then start fresh:
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
dropdb afro_caribbean_crm
createdb afro_caribbean_crm
python manage.py makemigrations
python manage.py migrate
```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints where possible
- Write docstrings for all functions

### Security Checklist Before Production
- [ ] Change DEBUG to False
- [ ] Set strong SECRET_KEY
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Enable HTTPS (SECURE_SSL_REDIRECT=True)
- [ ] Set up proper email backend
- [ ] Configure database backups
- [ ] Set up application monitoring
- [ ] Review rate limits
- [ ] Enable secure cookies

## 📄 License

Proprietary - All rights reserved

## 👥 Support

For questions or issues, contact: [Your Contact Information]

---

**Built with ❤️ for the African and Caribbean community**
