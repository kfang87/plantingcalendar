from plantingcalendarapp.helpers.data_fetcher import FarmSenseStation
from datetime import timedelta, datetime
from collections import defaultdict

class CalenderCalc:
    def __init__(self, last_frost_date:datetime, first_frost_date:datetime):
        self.WEEKS_FROM_LAST_FROST_MAP = {}
        self.last_frost_date = last_frost_date
        self.first_frost_date = first_frost_date

    def get_dates_from_last_frost(self) -> dict:
        for week in range(10, 0, -1):
            self.WEEKS_FROM_LAST_FROST_MAP[week] = self.last_frost_date  - timedelta(weeks=week)
        # import ipdb ; ipdb.set_trace()
        return self.WEEKS_FROM_LAST_FROST_MAP

