from werkzeug.exceptions import HTTPException
from flask import make_response
import json

class NotFoundError(HTTPException):
    def __init__(self, status_code):
        
        self.response = make_response('',status_code)

class BusninessValidationError(HTTPException):
    def __init__(self, status_code, error_message):
        message =  {'Error':error_message}
        self.response = make_response(json.dumps(message),status_code)
