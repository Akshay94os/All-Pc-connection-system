from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='home'), 
    path('api/register/', views.register_computer, name='register'),
    path('api/get-commands/<str:mac_address>/', views.get_pending_commands, name='get_commands'),
    # Add this new line:
    path('api/send-command/<str:mac_address>/', views.send_command, name='send_command'),
]