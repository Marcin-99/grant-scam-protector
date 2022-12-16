from django.contrib import admin
from .models import SuspiciousKeyword, AlertMessage

admin.site.register(SuspiciousKeyword)
admin.site.register(AlertMessage)
