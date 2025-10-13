# API Usage Examples

Complete examples for all API endpoints with real-world scenarios.

## Table of Contents
1. [Customer Registration Flow](#customer-registration-flow)
2. [Authentication Examples](#authentication-examples)
3. [Profile Management](#profile-management)
4. [Admin Operations](#admin-operations)

---

## Customer Registration Flow

### Scenario: New Customer Signs Up

**Step 1: Register**
```bash
curl -X POST http://localhost:8000/api/customers/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.johnson@email.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Sarah",
    "last_name": "Johnson",
    "phone_number": "+14165551234",
    "email_notifications": true,
    "sms_notifications": true,
    "push_notifications": true
  }'
```

**Response:**
```json
{
  "message": "Registration successful! Please check your email to verify your account.",
  "customer": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "email": "sarah.johnson@email.com",
    "first_name": "Sarah",
    "last_name": "Johnson",
    "full_name": "Sarah Johnson",
    "is_verified": false,
    "date_joined": "2024-10-12T10:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Step 2: Verify Email**

Customer receives email with verification link. They click it or you can verify programmatically:

```bash
curl -X POST http://localhost:8000/api/customers/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "verification-token-from-email"
  }'
```

---

## Authentication Examples

### Scenario: Customer Logs In

```bash
curl -X POST http://localhost:8000/api/customers/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sarah.johnson@email.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "message": "Login successful!",
  "customer": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "email": "sarah.johnson@email.com",
    "full_name": "Sarah Johnson",
    "is_verified": true,
    "total_purchases": 5,
    "loyalty_points": 150
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Scenario: Refresh Expired Access Token

```bash
curl -X POST http://localhost:8000/api/customers/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Profile Management

### Scenario: View Customer Profile

```bash
curl -X GET http://localhost:8000/api/customers/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "sarah.johnson@email.com",
  "first_name": "Sarah",
  "last_name": "Johnson",
  "full_name": "Sarah Johnson",
  "phone_number": "+14165551234",
  "street_address": "123 Main Street",
  "city": "Toronto",
  "province_state": "Ontario",
  "postal_code": "M1M 1M1",
  "country": "Canada",
  "dietary_preferences": "Vegetarian, No peanuts",
  "favorite_products": "Plantains, Jollof rice mix, Coconut milk",
  "email_notifications": true,
  "sms_notifications": true,
  "push_notifications": true,
  "total_purchases": 5,
  "loyalty_points": 150,
  "date_joined": "2024-10-12T10:30:00Z",
  "is_verified": true
}
```

### Scenario: Update Profile Information

```bash
curl -X PATCH http://localhost:8000/api/customers/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+14165559999",
    "street_address": "456 New Street",
    "city": "Toronto",
    "province_state": "Ontario",
    "postal_code": "M2M 2M2",
    "dietary_preferences": "Vegetarian, Halal",
    "favorite_products": "Plantains, Jollof rice, Suya spice, Coconut milk"
  }'
```

### Scenario: Update Notification Preferences

```bash
curl -X PATCH http://localhost:8000/api/customers/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email_notifications": true,
    "sms_notifications": false,
    "push_notifications": true
  }'
```

### Scenario: Change Password

```bash
curl -X POST http://localhost:8000/api/customers/change-password/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewSecure456!@",
    "new_password_confirm": "NewSecure456!@"
  }'
```

### Scenario: View Dashboard

```bash
curl -X GET http://localhost:8000/api/customers/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "profile": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "email": "sarah.johnson@email.com",
    "full_name": "Sarah Johnson"
  },
  "statistics": {
    "total_purchases": 5,
    "loyalty_points": 150,
    "member_since": "2024-10-12T10:30:00Z"
  },
  "notifications_enabled": {
    "email": true,
    "sms": false,
    "push": true
  }
}
```

---

## Admin Operations

### Scenario: Business Owner Views All Customers

```bash
curl -X GET http://localhost:8000/api/customers/admin/customers/ \
  -H "Authorization: Bearer STAFF_ACCESS_TOKEN"
```

**Response:**
```json
{
  "count": 125,
  "next": "http://localhost:8000/api/customers/admin/customers/?page=2",
  "previous": null,
  "results": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "email": "sarah.johnson@email.com",
      "full_name": "Sarah Johnson",
      "phone_number": "+14165551234",
      "city": "Toronto",
      "total_purchases": 5,
      "loyalty_points": 150,
      "is_verified": true,
      "date_joined": "2024-10-12T10:30:00Z",
      "last_login": "2024-10-12T14:20:00Z"
    },
    ...
  ]
}
```

### Scenario: Search for Specific Customers

```bash
# Search by name or email
curl -X GET "http://localhost:8000/api/customers/admin/customers/?search=sarah" \
  -H "Authorization: Bearer STAFF_ACCESS_TOKEN"

# Filter by verification status
curl -X GET "http://localhost:8000/api/customers/admin/customers/?is_verified=true" \
  -H "Authorization: Bearer STAFF_ACCESS_TOKEN"

# Filter by active status
curl -X GET "http://localhost:8000/api/customers/admin/customers/?is_active=true" \
  -H "Authorization: Bearer STAFF_ACCESS_TOKEN"
```

### Scenario: View Specific Customer Details

```bash
curl -X GET http://localhost:8000/api/customers/admin/customers/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Authorization: Bearer STAFF_ACCESS_TOKEN"
```

### Scenario: Add Note to Customer Profile

```bash
curl -X POST http://localhost:8000/api/customers/admin/customers/a1b2c3d4-e5f6-7890-abcd-ef1234567890/notes/ \
  -H "Authorization: Bearer STAFF_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "note": "Customer called about plantain availability. Prefers ripe plantains. Very friendly, regular shopper."
  }'
```

### Scenario: View All Notes for a Customer

```bash
curl -X GET http://localhost:8000/api/customers/admin/customers/a1b2c3d4-e5f6-7890-abcd-ef1234567890/notes/ \
  -H "Authorization: Bearer STAFF_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": "note-uuid-1",
    "customer": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "customer_name": "Sarah Johnson",
    "note": "Customer called about plantain availability. Prefers ripe plantains. Very friendly, regular shopper.",
    "created_by": "owner-uuid",
    "created_by_name": "Store Owner",
    "created_at": "2024-10-12T15:30:00Z",
    "updated_at": "2024-10-12T15:30:00Z"
  }
]
```

---

## Error Handling Examples

### Invalid Credentials
```bash
curl -X POST http://localhost:8000/api/customers/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "wrong@email.com",
    "password": "WrongPassword"
  }'
```

**Response (401):**
```json
{
  "error": "Invalid email or password."
}
```

### Weak Password
```bash
curl -X POST http://localhost:8000/api/customers/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "new@email.com",
    "password": "weak",
    "password_confirm": "weak",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Response (400):**
```json
{
  "password": [
    "This password is too short. It must contain at least 8 characters.",
    "The password must contain at least 1 digit.",
    "The password must contain at least 1 special character."
  ]
}
```

### Unauthorized Access
```bash
curl -X GET http://localhost:8000/api/customers/profile/
```

**Response (401):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Rate Limit Exceeded
After too many registration attempts:

**Response (429):**
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000/api/customers"

class CRMClient:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
    
    def register(self, email, password, first_name, last_name):
        response = requests.post(f"{BASE_URL}/register/", json={
            "email": email,
            "password": password,
            "password_confirm": password,
            "first_name": first_name,
            "last_name": last_name
        })
        if response.status_code == 201:
            data = response.json()
            self.access_token = data['tokens']['access']
            self.refresh_token = data['tokens']['refresh']
        return response.json()
    
    def login(self, email, password):
        response = requests.post(f"{BASE_URL}/login/", json={
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['tokens']['access']
            self.refresh_token = data['tokens']['refresh']
        return response.json()
    
    def get_profile(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        return response.json()
    
    def update_profile(self, **kwargs):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.patch(f"{BASE_URL}/profile/", 
                                 json=kwargs, 
                                 headers=headers)
        return response.json()

# Usage
client = CRMClient()
client.register("test@example.com", "SecurePass123!", "Test", "User")
profile = client.get_profile()
print(f"Welcome, {profile['full_name']}!")
```

---

## JavaScript/React Example

```javascript
const API_URL = 'http://localhost:8000/api/customers';

// Register new customer
async function register(email, password, firstName, lastName) {
  const response = await fetch(`${API_URL}/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      password,
      password_confirm: password,
      first_name: firstName,
      last_name: lastName
    })
  });
  
  const data = await response.json();
  if (response.ok) {
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
  }
  return data;
}

// Login
async function login(email, password) {
  const response = await fetch(`${API_URL}/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  if (response.ok) {
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
  }
  return data;
}

// Get profile
async function getProfile() {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${API_URL}/profile/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
}

// Update profile
async function updateProfile(updates) {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${API_URL}/profile/`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  return response.json();
}
```

---

## Postman Collection

Import this JSON into Postman for easy testing:

1. Open Postman
2. Click "Import"
3. Copy and paste the API endpoints
4. Set up environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: (will be set after login)

Happy testing! 🚀
