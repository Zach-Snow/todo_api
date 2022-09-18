from flask_restful import Resource
from flask import request
from typing import Dict


class Root(Resource):
    def get(self) -> Dict:
        return {
            "service": "TO-DO API",
            "version": "1",
            "status": "online"
        }
