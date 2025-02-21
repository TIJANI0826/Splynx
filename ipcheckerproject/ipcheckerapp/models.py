from django.db import models
from django.utils.timezone import now

# Create your models here.

class UserIP(models.Model):
    username = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=50, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)  # Track last update time

    def is_online(self):
        """A user is online if their last update was within the last 5 minutes."""
        return (now() - self.last_updated).total_seconds() < 300  # 5 minutes

    def __str__(self):
        return f"{self.username} - {self.ip_address} ({self.latitude}, {self.longitude})"

    def __str__(self):
        return f"{self.username} - {self.ip_address} ({self.latitude}, {self.longitude})"
