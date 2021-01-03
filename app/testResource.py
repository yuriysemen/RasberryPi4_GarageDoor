from typing import Dict

from flask_restful import Resource


class TestResource(Resource):
    """Rules resource."""

    def get(self) -> Dict:
        return {
            "code": "success",
            "message": "Hello"
        }
