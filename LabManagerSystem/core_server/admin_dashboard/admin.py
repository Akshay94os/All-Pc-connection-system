from django.contrib import admin
from .models import LabComputer, CommandLog

admin.site.register(LabComputer)
admin.site.register(CommandLog)