
from django.urls import path
from . import views

urlpatterns = [
    # This is your new homepage!
    path('', views.dashboard_home, name='home'), 
    
    # This is your existing API doorway
    path('api/register/', views.register_computer, name='register'),
]