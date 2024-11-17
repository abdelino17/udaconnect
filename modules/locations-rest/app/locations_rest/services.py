import logging
from typing import Dict
import json

from flask import g
from app.locations_rest.schemas import LocationSchema

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locations-rest-api")


class LocationService:
    @staticmethod
    def create(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        print("----------reached")
        data = json.dumps(location).encode("utf-8")
        kafka_producer = g.kafka_producer
        kafka_producer.send(g.kafka_topic, value=data)
        kafka_producer.flush()
        print("published to kafka topic")
