# ========================================
# ADD THESE LINES TO config/settings.py
# ========================================

# CRITICAL: Add this near the top with other imports
import os
from pathlib import Path

# CRITICAL: Update these existing settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-temp-key-change-in-production')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CRITICAL: Add CSRF_TRUSTED_ORIGINS (NEW - fixes the 403 error)
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-da16.up.railway.app',
    'https://*.railway.app',
]

# If you have a custom domain later, add it too:
# CSRF_TRUSTED_ORIGINS = [
#     'https://web-production-da16.up.railway.app',
#     'https://*.railway.app',
#     'https://yourdomain.com',
# ]

# CRITICAL: Update MIDDLEWARE to include WhiteNoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← ADD THIS LINE (after SecurityMiddleware)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CRITICAL: Add STATIC files configuration
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Optional but recommended: Update CORS settings if you have them
CORS_ALLOWED_ORIGINS = [
    'https://web-production-da16.up.railway.app',
]