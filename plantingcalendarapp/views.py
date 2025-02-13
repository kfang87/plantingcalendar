from django.http import HttpResponse
from plantingcalendarapp.helpers.data_fetcher import PHZmapi, FarmSenseStation
from plantingcalendarapp.helpers.calendar_calc import CalenderCalc

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
        cc = CalenderCalc(last_frost_date=fs.last_frost_date, first_frost_date=fs.first_frost_date)
        calendar_dates = cc.get_dates_from_last_frost()

    zone_frost = {
        "zip_code": zip_code,
        "zone": phzmapi.zone,
        "station_name" : fs.name,
        "first_frost_date": fs.first_frost_date,
        "last_frost_date": fs.last_frost_date,
        "frost_calendar_dict": calendar_dates,
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


