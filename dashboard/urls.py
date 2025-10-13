from django.urls import path
from django.http import HttpResponse
from . import views

# Simple test view
def test_view(request):
    return HttpResponse("🎉 Dashboard app is working!")

app_name = 'dashboard'

urlpatterns = [
    path('test/', test_view, name='test'),
    path('register/', views.customer_register, name='register'),
    path('login/', views.customer_login_view, name='login'),
    path('logout/', views.customer_logout_view, name='logout'),
    path('', views.dashboard_home, name='home'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('profile/', views.profile_view, name='profile'),  # ADD THIS LINE
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # ADD THIS LINE TOO
]