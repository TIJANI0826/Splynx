from django.db import models
from django.utils.timezone import now

# Create your models here.
class UserIP(models.Model):
    username = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_online = models.BooleanField(default=False)  # Track active sessions
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.ip_address}"
