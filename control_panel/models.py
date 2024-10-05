from django.db import models

class LockScreen(models.Model):
    logo = models.FileField(upload_to='lock_screens/')
    is_active = models.BooleanField(default=False)  # To track the active lock screen

class DomainNotification(models.Model):
    domain = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # To enable/disable specific domains
