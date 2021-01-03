from typing import Dict

from flask_restful import Resource
from app import door


class TestResource(Resource):
    """Rules resource."""

    def get(self) -> Dict:
        door.open()
        return {
            "code": "success",
            "state": door.state
        }
