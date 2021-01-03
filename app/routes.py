from app.testResource import TestResource


def init_routes(api) -> None:
    """
    Add all available resources to api.

    :param api: Flask API app
    """
    api.add_resource(TestResource, "/test")
