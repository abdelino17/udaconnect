import logging
from typing import Dict
import json
import sys
import os

import grpc
from app.locations_grpc.schemas import LocationSchema
from app.config import config_by_name

import app.location_pb2_grpc as rpc

if sys.version_info >= (3, 12, 0):
    import six

    sys.modules["kafka.vendor.six.moves"] = six.moves

from kafka import KafkaProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("locations-rest-api")


CONFIG = config_by_name[os.getenv("ENV", "test")]

kafka_producer = KafkaProducer(
    bootstrap_servers=CONFIG.KAFKA_BROKER,
)


class LocationService(rpc.LocationServiceServicer):
    def Create(self, request, context):
        payload = {
            "person_id": str(request.person_id),
            "longitude": str(request.longitude),
            "latitude": str(request.latitude),
            "creation_time": str(request.creation_time),
        }
        print(request.creation_time)

        logging.info("location: %r", request)
        validation_results: Dict = LocationSchema().validate(payload)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid payload: {validation_results}")
            raise ValueError("Invalid payload")

        data = json.dumps(payload).encode("utf-8")
        kafka_producer.send(CONFIG.KAFKA_TOPIC, value=data)
        kafka_producer.flush()
        print("published to kafka topic")
        return request
