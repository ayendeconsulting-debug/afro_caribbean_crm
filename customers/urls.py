"""
URL Configuration for customers app
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'customers'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Customer profile endpoints
    path('profile/', views.CustomerProfileView.as_view(), name='profile'),
    path('dashboard/', views.CustomerDashboardView.as_view(), name='dashboard'),
    
    # Health check
    path('health/', views.HealthCheckView.as_view(), name='health'),
]