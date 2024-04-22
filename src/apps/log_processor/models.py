from datetime import datetime

from django.db import models


class NginxLogEntry(models.Model):
    ip_address = models.CharField(max_length=45, null=True)
    date = models.DateTimeField(
        null=True, default=datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    )
    http_method = models.CharField(max_length=10, null=True)
    request_uri = models.TextField(null=True)
    response_code = models.IntegerField(null=True)
    response_size = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.date} - {self.ip_address}"
