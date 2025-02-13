from plantingcalendarapp.helpers.data_fetcher import FarmSenseStation
from plantingcalendarapp.models import  GrowerCalendar, GrowerPlantingEvent
from datetime import timedelta, datetime
from collections import defaultdict


def get_dates_from_last_frost(calendar: GrowerCalendar) -> dict:
    calendar_frost_mapping = {}
    for week in range(10, 0, -1):
        calendar_frost_mapping[week] = calendar.last_frost_date  - timedelta(weeks=week)
    # import ipdb ; ipdb.set_trace()
    return calendar_frost_mapping

# def create_planting_events_for_grower_calendar(calendar: GrowerCalendar) -> list(PlantingEvent):

