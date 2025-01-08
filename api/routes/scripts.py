import logging
from flask import jsonify, request
import hashlib
import json
from api.routes.api_routes_logging import setup_logger

setup_logger()


def get_cache_key():
    sport_type = request.view_args.get('sport_type')
    logging.info(f"Cache key for sport type: {sport_type}")
    return f"sport_stream_{sport_type}"


def post_cache_key():
    json_data = request.get_json(silent=True) or {}
    json_string = json.dumps(json_data, sort_keys=True)
    hashed_key = hashlib.md5(json_string.encode('utf-8')).hexdigest()
    logging.info(f"Generated cache key: {hashed_key} for method {request.method} on path {request.path}")
    return f"{request.method}:{request.path}:{hashed_key}"


def check_positive_param(param_name):
    param_value = request.args.get(param_name, type=int)
    if param_value is None or param_value <= 0:
        logging.warning(f"Invalid parameter value for {param_name}: {param_value}")
        return False
    logging.info(f"Valid parameter value for {param_name}: {param_value}")
    return True
