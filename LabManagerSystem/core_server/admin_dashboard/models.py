from django.db import models

class LabComputer(models.Model):
    hostname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, unique=True)
    os_version = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

class CommandLog(models.Model):
    computer = models.ForeignKey(LabComputer, on_delete=models.CASCADE)
    command = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)