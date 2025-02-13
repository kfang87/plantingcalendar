import requests
import json
from datetime import date

class PHZmapi:

    def __init__(self):
        self.zone = None
        self.temperature_range = None
        self.coordinate_lat = None
        self.coordinate_long = None


    def load_phzmapi_data(self, zip_code):
        BASE_URL = 'https://phzmapi.org'
        api_url = f"{BASE_URL}/{zip_code}.json"
        response = requests.get(api_url).json()
        # import ipdb; ipdb.set_trace()
        self.zone = response['zone']
        self.temperature_range = response['temperature_range']
        self.coordinate_lat = response['coordinates']['lat']
        self.coordinate_long = response['coordinates']['lon']

class FarmSenseStation:
    def __init__(self):
        self.farmsense_id = None
        self.name = None
        self.coordinate_lat = None
        self.coordinate_long = None
        self.first_frost_date = None
        self.last_frost_date = None

    def load_stations_from_coordinates(self, origin_coordinate_lat, origin_coordinate_long):
        BASE_URL = "https://api.farmsense.net/v1/frostdates/stations"
        # import ipdb; ipdb.set_trace()
        api_url = f"{BASE_URL}/?lat={origin_coordinate_lat}&lon={origin_coordinate_long}"
        response = requests.get(api_url).json()
        station = None
        if len(response) > 0:
            station = response[0]
        self.farmsense_id = station['id']
        self.name = station['name']
        self.coordinate_lat = station['lat']
        self.coordinate_long = station['lon']


    def load_frost_data_for_station(self, farmsense_station_id):
        BASE_URL = "https://api.farmsense.net/v1/frostdates/probabilities"
        INDEX_THRESHOLD_36 = 0
        INDEX_THRESHOLD_32 = 1
        PCT_THRESHOLD = 'prob_20' # 20% chance that frost would occur after this date in Spring
                                # or before this date in Autumn

        SEASON_SPRING = 1
        SEASON_FALL = 2

        api_url_spring = f"{BASE_URL}/?station={farmsense_station_id}&season={SEASON_SPRING}"
        api_url_autumn= f"{BASE_URL}/?station={farmsense_station_id}&season={SEASON_FALL}"
        response_spring = requests.get(api_url_spring).json()
        response_autumn = requests.get(api_url_autumn).json()

        last_frost_date_raw = response_spring[INDEX_THRESHOLD_32][PCT_THRESHOLD]
        first_frost_date_raw = response_autumn[INDEX_THRESHOLD_32][PCT_THRESHOLD]

        self.last_frost_date = date(month=int(last_frost_date_raw[:2]), day=int(last_frost_date_raw[2:]), year=2025)
        self.first_frost_date = date(month=int(first_frost_date_raw[:2]), day=int(first_frost_date_raw[2:]), year=2025)