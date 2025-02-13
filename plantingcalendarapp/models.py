from django.db import models

# Create your models here.

class USDAHardinessZone(models.Model):
    zone = models.CharField(max_length=10)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.zone}: {self.description}"

class PlantingEvent(models.Model):
    event_code = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.event_code}"