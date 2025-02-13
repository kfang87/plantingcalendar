from IPython.core.completerlib import module_completer
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

# Universal models
class USDAHardinessZone(models.Model):
    zone = models.CharField(max_length=10)
    description = models.CharField(max_length=1000)

    objects = models.Manager()

    def __str__(self):
        return f"{self.zone}: {self.description}"

class PlantSpecies(models.Model):
    name = models.CharField(max_length=200, default="")
    binomial = models.CharField(max_length=1000, default="")
    website =  models.CharField(max_length=1000, default="", null=True)
    needs_cold_stratify = models.BooleanField(default=False)
    needs_indoor_sow = models.BooleanField(default=False)
    can_direct_sow = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.name} ({self.binomial})"

# Plant Species subtype: Requires cold stratification
class PlantSpeciesColdStratify(PlantSpecies):
    cold_stratify_days_before_transplant = models.IntegerField()
    transplant_days_before_last_frost = models.IntegerField(default=0)

    objects = models.Manager()

# Plant Species subtype
class PlantSpeciesIndoorSow(PlantSpecies):
    indoor_sow_weeks_before_last_frost_min = models.IntegerField()
    indoor_sow_weeks_before_last_frost_max = models.IntegerField()
    objects = models.Manager()



# Plant Species subtype: Direct sow
class PlantSpeciesDirectSow(PlantSpecies):
    sow_weeks_before_last_frost = models.IntegerField()
    objects = models.Manager()




# Models for specific grower calendar

class Grower(models.Model):
    username = models.CharField(max_length=100, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.username

class GrowerCalendar(models.Model):
    name = models.CharField(max_length=1000)
    grower = models.ForeignKey(
        Grower,
        models.PROTECT,
        blank=True,
        null=True
    )
    last_frost_date = models.DateTimeField()
    first_frost_date = models.DateTimeField()
    usda_hardiness_zone = models.ForeignKey(
        USDAHardinessZone,
        models.PROTECT,
        blank=True,
        null=True
    )
    station_id = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return f"{self.grower} {self.station_id} {self.name}"

    class Meta:
        unique_together = ('grower', 'station_id')

class GrowerPlant(models.Model):
    grower_calendar = models.ForeignKey(
        GrowerCalendar,
        models.PROTECT,
        blank=True,
        null=True
    )

    plant_species = models.ForeignKey(
        PlantSpecies,
        models.PROTECT,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('grower_calendar', 'plant_species')

    objects = models.Manager()


class GrowerPlantingEvent(models.Model):
    class PlantingEventType(models.TextChoices):
        INDOOR_SOW = 'INDOOR_SOW', _('Indoor sow')
        DIRECT_SOW = 'DIRECT_SOW', _('Direct sow outdoors')
        TRANSPLANT = 'TRANSPLANT', _('Transplant outdoors')
        COLD_STRATIFY = 'COLD_STRATIFY', _('Cold stratify')

    calendar = models.ForeignKey(
        GrowerCalendar,
        models.PROTECT,
        blank=True,
        null=True
    )
    event_type = models.CharField(max_length=100, choices=PlantingEventType, default=PlantingEventType.DIRECT_SOW)
    plant = models.ForeignKey(
        GrowerPlant,
        models.PROTECT,
        blank = True,
        null = True
    )
    event_code = models.CharField(max_length=200, default="")
    title = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=1000, default="")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    objects = models.Manager()

    def __str__(self):
        return f"{self.event_code}"

    class Meta:
        unique_together = ('plant', 'event_type')