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
    import ipdb; ipdb.set_trace()
    event_list = []
    # get all plants on the grower calendar
    grower_plants = GrowerPlant.objects.filter(grower_calendar=grower_calendar)
    for gp in grower_plants:
        # if direct sow, create direct sow event
        if gp.plant_species.can_direct_sow:
            #sowing event for direct sow days minus last frost
            description = f"{GrowerPlantingEvent.PlantingEventType.DIRECT_SOW.name} {gp.plant_species}"
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.DIRECT_SOW,
                plant=gp,
                # descriptive fields
                event_code="",
                title=description,
                description=description,
                start_datetime=grower_calendar.last_frost_date - timedelta(
                    days=gp.plant_species.plantspeciesdirectsow.sow_days_before_last_frost),
                end_datetime=grower_calendar.last_frost_date,
            )
            event_list.append(description)
        elif gp.plant_species.needs_indoor_sow:
            # sowing event for indoor sow days minus transplant
            indoor_sow_description = f"{GrowerPlantingEvent.PlantingEventType.INDOOR_SOW.name} {gp.plant_species}"
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.INDOOR_SOW,
                plant=gp,
                # descriptive fields
                event_code="",
                title=indoor_sow_description,
                description=indoor_sow_description,
                start_datetime=grower_calendar.last_frost_date - timedelta(
                    days=gp.plant_species.plantspeciesindoorsow.indoor_sow_days_before_last_frost_max),
                end_datetime=grower_calendar.last_frost_date - timedelta(
                    days=gp.plant_species.plantspeciesindoorsow.indoor_sow_days_before_last_frost_min),
            )
            event_list.append(indoor_sow_description)

            # transplant event for transplant days minus last frost
            transplant_description = f"{GrowerPlantingEvent.PlantingEventType.TRANSPLANT.name} {gp.plant_species}"
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.TRANSPLANT,
                plant=gp,
                # descriptive fields
                event_code="",
                title=transplant_description,
                description=transplant_description,
                start_datetime=grower_calendar.last_frost_date,
                end_datetime=grower_calendar.last_frost_date,
            )
            event_list.append(transplant_description)

            pass
        elif gp.plant_species.needs_cold_stratify:

            # cold stratify event for cold sow minus transplant
            cold_stratify_description = f"{GrowerPlantingEvent.PlantingEventType.COLD_STRATIFY.name} {gp.plant_species}"
            transplant_date =  grower_calendar.last_frost_date - timedelta(days=gp.plant_species.plantspeciescoldstratify.transplant_days_before_last_frost)
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.COLD_STRATIFY,
                plant=gp,
                # descriptive fields
                event_code="",
                title=cold_stratify_description,
                description=cold_stratify_description,
                start_datetime=transplant_date - timedelta(
                    days=gp.plant_species.plantspeciescoldstratify.cold_stratify_days_before_transplant),
                end_datetime=transplant_date - timedelta(
                    days=gp.plant_species.plantspeciescoldstratify.cold_stratify_days_before_transplant),
            )
            event_list.append(cold_stratify_description)

            # transplant event for transplant days minus last frost
            transplant_description = f"{GrowerPlantingEvent.PlantingEventType.TRANSPLANT.name} {gp.plant_species}"
            gpe = GrowerPlantingEvent.objects.update_or_create(
                # unique together fields
                calendar=grower_calendar,
                event_type=GrowerPlantingEvent.PlantingEventType.TRANSPLANT,
                plant=gp,
                # descriptive fields
                event_code="",
                title=transplant_description,
                description=transplant_description,
                start_datetime=transplant_date,
                end_datetime=transplant_date,
            )
            event_list.append(transplant_description)
    print(event_list)
