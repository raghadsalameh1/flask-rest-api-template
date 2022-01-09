from flask import Blueprint, jsonify
from src.constants import http_status_codes as status
from werkzeug.exceptions import HTTPException

debug = True # Switch it to False in production

errors = Blueprint("errors",__name__)

@errors.app_errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors. You wouldn't want to handle these generically.
    if isinstance(e, HTTPException):
        return e
    
    # now you're handling non-HTTP exceptions only
    res = {
           'error': 'Something went wrong, we are working on it'}
    if debug:
        res['errorMessage'] = e.message if hasattr(e, 'message') else f'{e}'
    return jsonify(res), status.HTTP_500_INTERNAL_SERVER_ERROR

@errors.app_errorhandler(status.HTTP_404_NOT_FOUND)
def handle404(e):
    return jsonify({"error":"Not found"}),status.HTTP_404_NOT_FOUND

@errors.app_errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def handle405(e):
    return jsonify({"error":"Method not allowed"}),status.HTTP_405_METHOD_NOT_ALLOWED



