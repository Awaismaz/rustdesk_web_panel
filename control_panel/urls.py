from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard linked to the home URL
    path('upload/', views.upload_logo, name='upload_logo'),
    path('manage/', views.manage_lock_screens, name='manage_lock_screens'),
    path('domains/', views.manage_domains, name='manage_domains'),
    path('api/lock_screen/', views.get_active_lock_screen, name='get_active_lock_screen'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)