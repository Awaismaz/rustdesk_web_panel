from django.contrib import admin
from .models import LockScreen, DomainNotification, ConnectedClient

admin.site.register(LockScreen)
admin.site.register(DomainNotification)
admin.site.register(ConnectedClient)
