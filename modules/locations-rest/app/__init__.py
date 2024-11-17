from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
import sys

if sys.version_info >= (3, 12, 0):
    import six

    sys.modules["kafka.vendor.six.moves"] = six.moves

from kafka import KafkaProducer


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    CONFIG = config_by_name[env or "test"]

    app = Flask(__name__)
    app.config.from_object(CONFIG)
    api = Api(app, title="Locations-Rest API", version="1.0.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)

    @app.before_request
    def before_request():
        producer = KafkaProducer(bootstrap_servers=CONFIG.KAFKA_BROKER)
        g.kafka_producer = producer
        g.kafka_topic = CONFIG.KAFKA_TOPIC

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
