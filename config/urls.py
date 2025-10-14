from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.http import HttpResponse
from django.shortcuts import redirect

def root_view(request):
    """Redirect root URL to dashboard login"""
    return redirect('dashboard:login')

urlpatterns = [
    # Dashboard MUST come BEFORE admin
    path('', root_view),  # ← ADD THIS LINE FIRST
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/messages/', include('messaging.urls')),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/customers/', include('customers.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]