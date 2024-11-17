from app.persons_api.models import Connection, Location, Person  # noqa
from app.persons_api.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.persons_api.controllers import api as udaconnect_api

    api.add_namespace(udaconnect_api, path=f"/{root}")
