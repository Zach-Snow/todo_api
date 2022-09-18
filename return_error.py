import json
from typing import Dict
from flask import Response,jsonify

def return_error(status:int) -> Dict:
    error_message = {"Error": "There was an error loading the To-Do objects."}
    byte_format = json.dumps(error_message)
    return Response(byte_format, status=status, mimetype='application/json')
