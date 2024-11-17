import json
import sys

if sys.version_info >= (3, 12, 0):
    import six

    sys.modules["kafka.vendor.six.moves"] = six.moves

from app.locations_worker.services import LocationService
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def start(env=None):
    from app.config import config_by_name

    CONFIG = config_by_name[env or "test"]

    consumer = KafkaConsumer(
        CONFIG.KAFKA_TOPIC,
        bootstrap_servers=CONFIG.KAFKA_BROKER,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    loc_service = LocationService()

    engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)

    for message in consumer:
        print(message.value["person_id"])
        try:
            loc_service.create(message.value, session=Session())
        except Exception as e:
            print(f"Error processing message {message.value}: {e}")
            continue
        print(f"Message {message.value} has been processed!")
