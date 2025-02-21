from django.contrib import admin

# Register your models here
from .models import UserIP
admin.site.register(UserIP)
# Compare this snippet from ipcheckerproject/ipcheckerapp/views.py: