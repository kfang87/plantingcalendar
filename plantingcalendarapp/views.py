from django.http import HttpResponse

from plantingcalendarapp.helpers.data_fetcher import PHZmapi, FarmSenseStation
from plantingcalendarapp.models import *
from plantingcalendarapp.helpers.calendar_utils import get_dates_from_last_frost, create_planting_events_for_grower_calendar

def index(request):
    return HttpResponse("Hello, world. You're at Planting Calendar app.")


from django.shortcuts import render
from django.template import loader

# Create your views here.

def calendar(request, zip_code):
    phzmapi = PHZmapi()
    phzmapi.load_phzmapi_data(zip_code)
    calendar_dates = None

    fs = FarmSenseStation()
    fs.load_stations_from_coordinates(phzmapi.coordinate_lat, phzmapi.coordinate_long)
    if fs.farmsense_id:
        fs.load_frost_data_for_station(fs.farmsense_id)


    if fs.last_frost_date:
        zone = USDAHardinessZone.objects.get(zone=phzmapi.zone)
        # import ipdb; ipdb.set_trace()
        grower = Grower.objects.get(username='kayla')
        station_id = int(fs.farmsense_id)
        gc, created = GrowerCalendar.objects.get_or_create(
                grower=grower,
                station_id=station_id,
                name=f"Zone: {phzmapi.zone}; Station: {fs.farmsense_id} [{fs.name}]",
                last_frost_date=fs.last_frost_date,
                first_frost_date=fs.first_frost_date,
                usda_hardiness_zone=zone,
            )
        calendar_dates = get_dates_from_last_frost(gc)
        grower_planting_events = create_planting_events_for_grower_calendar(gc)

    zone_frost = {
        "zip_code": zip_code,
        "zone": phzmapi.zone,
        "station_name" : fs.name,
        "first_frost_date": fs.first_frost_date,
        "last_frost_date": fs.last_frost_date,
        "frost_calendar_dict": calendar_dates,
        "grower_planting_events": grower_planting_events
    }

    template = loader.get_template("plantingcalendarapp/index.html")
    context = {"zone_frost": zone_frost}
    return HttpResponse(template.render(context, request))


    # return HttpResponse(f"Your planting calendar for zip code {zip_code} "
    #                     f"with in zone {phzmapi.zone}"
    #                     f"\n\n\n"
    #                     f"Your nearest station is in {fs.name}"
    #                     f"Your last frost date in Spring is {fs.last_frost_date}"
    #                     f"Your first frost date in Autumn is {fs.first_frost_date}")


