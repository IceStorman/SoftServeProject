from flask import jsonify, request
from flask import request
import hashlib
import json

def get_error_response(e, status_code):
    return jsonify(e), status_code

def get_good_response(result):
    return result, 200


def get_cache_key():
   sport_type = request.view_args.get('sport_type')
   return f"sport_stream_{sport_type}"


def post_cache_key():
    json_data = request.get_json(silent=True) or {}
    json_string = json.dumps(json_data, sort_keys=True)
    return f"{request.method}:{request.path}:{hashlib.md5(json_string.encode('utf-8')).hexdigest()}"


def check_positive_param(param_name):
    param_value = request.args.get(param_name, type=int)
    if param_value is None or param_value <= 0:
        return False
    return True
