from app.locations_rest.services import (
    LocationService,
    LocationSchema,
)

from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("LocationsRest", description="Locations REST API for mobile devices.")


@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Response:
        LocationService.create(request.get_json())
        return Response(status=201)
