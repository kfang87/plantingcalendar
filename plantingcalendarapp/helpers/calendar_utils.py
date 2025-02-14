from plantingcalendarapp.helpers.data_fetcher import FarmSenseStation
from plantingcalendarapp.models import  *
from datetime import timedelta, datetime
from collections import defaultdict


def get_dates_from_last_frost(calendar: GrowerCalendar) -> dict:
    calendar_frost_mapping = {}
    for week in range(10, 0, -1):
        calendar_frost_mapping[week] = calendar.last_frost_date  - timedelta(weeks=week)
    # import ipdb ; ipdb.set_trace()
    return calendar_frost_mapping

def create_planting_events_for_grower_calendar(grower_calendar: GrowerCalendar) :
    # import ipdb; ipdb.set_trace()
    event_list = []
    # get all plants on the grower calendar
    grower_plants = GrowerPlant.objects.filter(grower_calendar=grower_calendar)
    for gp in grower_plants:
        # if direct sow, create direct sow event
        if gp.plant_species.can_direct_sow:
            #sowing event for direct sow days minus last frost
            description = f"""
            {gp.plant_species.name} can be sown directly outdoors {gp.plant_species.plantspeciesdirectsow.sow_weeks_before_last_frost} weeks before the last frost date.
"""
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.DIRECT_SOW,
                plant=gp,
                # descriptive fields
                defaults={
                    'event_code':"",
                'title': description,
                'description': description,
                'start_datetime': grower_calendar.last_frost_date - timedelta(
                    weeks=gp.plant_species.plantspeciesdirectsow.sow_weeks_before_last_frost),
                'end_datetime': grower_calendar.last_frost_date,
            })
            event_list.append(description)
        elif gp.plant_species.needs_indoor_sow:
            # sowing event for indoor sow days minus transplant
            indoor_sow_description = f"""
            {gp.plant_species.name} can be sown indoors {gp.plant_species.plantspeciesindoorsow.indoor_sow_weeks_before_last_frost_min} to {gp.plant_species.plantspeciesindoorsow.indoor_sow_weeks_before_last_frost_max} weeks before the last frost date.
            This will ensure the growing season is long enough.  
"""
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.INDOOR_SOW,
                plant=gp,
                # descriptive fields
                defaults={
                    'event_code': "",
                'title': indoor_sow_description,
                'description': indoor_sow_description,
                'start_datetime': grower_calendar.last_frost_date - timedelta(
                    weeks=gp.plant_species.plantspeciesindoorsow.indoor_sow_weeks_before_last_frost_max),
                'end_datetime': grower_calendar.last_frost_date - timedelta(
                    weeks=gp.plant_species.plantspeciesindoorsow.indoor_sow_weeks_before_last_frost_min),
                }
            )
            event_list.append(indoor_sow_description)

            # transplant event for transplant days minus last frost
            transplant_description = f"""
            Your indoor {gp.plant_species.name} should be transplanted outside after your last frost date.
            """
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.TRANSPLANT,
                plant=gp,
                # descriptive fields
                defaults={
                    'event_code': "",
                'title': transplant_description,
                'description': transplant_description,
                'start_datetime': grower_calendar.last_frost_date,
                'end_datetime': grower_calendar.last_frost_date,
            })
            event_list.append(transplant_description)

            pass
        elif gp.plant_species.needs_cold_stratify:

            # cold stratify event for cold sow minus transplant
            cold_stratify_description = f"""
            {gp.plant_species.name} needs to have a {gp.plant_species.plantspeciescoldstratify.cold_stratify_days_before_transplant} day period of cold stratification before being transplanted into the ground.
            This plant can be transplanted {gp.plant_species.plantspeciescoldstratify.transplant_days_before_last_frost} days before the last frost.
"""
            transplant_date =  grower_calendar.last_frost_date - timedelta(days=gp.plant_species.plantspeciescoldstratify.transplant_days_before_last_frost)
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.COLD_STRATIFY,
                plant=gp,
                # descriptive fields
                defaults = { 'event_code':"",
                'title':cold_stratify_description,
                'description':cold_stratify_description,
                'start_datetime':transplant_date - timedelta(
                    days=gp.plant_species.plantspeciescoldstratify.cold_stratify_days_before_transplant),
                'end_datetime':transplant_date - timedelta(
                    days=gp.plant_species.plantspeciescoldstratify.cold_stratify_days_before_transplant),
            }
            )
            event_list.append(cold_stratify_description)

            # transplant event for transplant days minus last frost
            transplant_description = f"""
            Your cold stratified {gp.plant_species.name} is ready to be transplanted to the ground once the risk of frost as passed.
"""
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.TRANSPLANT,
                plant=gp,
                # descriptive fields
                defaults={
                    'event_code': "",
                'title': transplant_description,
                'description': transplant_description,
                'start_datetime': transplant_date,
                'end_datetime': transplant_date,
                }
            )
            event_list.append(transplant_description)
    return GrowerPlantingEvent.objects.filter(calendar=grower_calendar).order_by('start_datetime')
