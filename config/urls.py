# ========================================
# UPDATE config/urls.py
# ========================================

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse

# Simple root view - redirects to dashboard
def root_view(request):
    """Redirect root URL to dashboard"""
    return redirect('dashboard:login')

# Alternative: Show a welcome page
def welcome_view(request):
    """Simple welcome page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Afro-Caribbean CRM</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                text-align: center;
                padding: 2rem;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            a {
                display: inline-block;
                margin: 10px;
                padding: 12px 24px;
                background: #FFD700;
                color: #333;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }
            a:hover {
                background: #FFC700;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 Afro-Caribbean CRM</h1>
            <p>Welcome to the Customer Relationship Management System</p>
            <div>
                <a href="/dashboard/register/">Register</a>
                <a href="/dashboard/login/">Login</a>
                <a href="/admin/">Admin Panel</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    # Root URL - choose one option:
    path('', root_view),  # Option 1: Redirect to dashboard login
    # path('', welcome_view),  # Option 2: Show welcome page (comment out line above, uncomment this)
    
    # Dashboard and messaging
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/messages/', include('messaging.urls')),
    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('customers.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]