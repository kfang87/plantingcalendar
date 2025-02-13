from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(USDAHardinessZone)
admin.site.register(PlantSpecies)
admin.site.register(PlantSpeciesColdStratify)
admin.site.register(PlantSpeciesIndoorSow)
admin.site.register(PlantSpeciesDirectSow)

admin.site.register(Grower)
admin.site.register(GrowerCalendar)
admin.site.register(GrowerPlant)
admin.site.register(GrowerPlantingEvent)
