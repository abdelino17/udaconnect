import logging
from typing import Dict

from app.locations_worker.models import Location
from app.locations_worker.schemas import LocationSchema
from geoalchemy2.functions import ST_Point

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locations-worker-api")


class LocationService:
    @staticmethod
    def create(location: Dict, session) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        session.add(new_location)
        session.commit()

        return new_location
