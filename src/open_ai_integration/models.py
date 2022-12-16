from django.db import models


class AlertMessage(models.Model):
    fullText = models.CharField(max_length=16384)
    summary = models.CharField(max_length=2048)
    summaryItemColor = models.CharField(max_length=8)


class SuspiciousKeyword(models.Model):
    keyword = models.CharField(max_length=128)
    weight = models.FloatField()
    alertMessage = models.ForeignKey(AlertMessage, on_delete=models.CASCADE)
