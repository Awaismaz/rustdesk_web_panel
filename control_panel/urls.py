from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard linked to the home URL
    path('upload/', views.upload_logo, name='upload_logo'),
    path('manage/', views.manage_lock_screens, name='manage_lock_screens'),
    path('domains/', views.manage_domains, name='manage_domains'),
    path('api/lock_screen/', views.get_active_lock_screen, name='get_active_lock_screen'),
]

