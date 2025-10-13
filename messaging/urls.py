from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('thread/<int:thread_id>/', views.thread_view, name='thread'),
    path('thread/<int:thread_id>/close/', views.close_thread, name='close_thread'),
]
