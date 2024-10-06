from django.db import models

class LockScreen(models.Model):
    logo = models.FileField(upload_to='lock_screens/')
    is_active = models.BooleanField(default=False)  # To track the active lock screen

class DomainNotification(models.Model):
    domain = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # To enable/disable specific domains


class ConnectedClient(models.Model):
    client_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    status = models.CharField(max_length=50, choices=[('connected', 'Connected'), ('disconnected', 'Disconnected')], default='connected')
    last_seen = models.DateTimeField(auto_now=True)
    last_domain_accessed= models.CharField(max_length=255, default='www.google.com')
    systemname= models.CharField(max_length=255, default='unknown')
    OS= models.CharField(max_length=255, default='unknown')
    
    def __str__(self):
        return f"{self.name} ({self.client_id})"