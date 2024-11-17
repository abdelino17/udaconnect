def register_routes(api, app, root="api"):
    from app.locations_rest import register_routes as attach_locations_rest

    # Add routes
    attach_locations_rest(api, app)
