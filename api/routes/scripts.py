from flask import request
import hashlib
import json
from logger.logger import Logger

logger = Logger("logger", "all.log")



def get_cache_key():
    sport_type = request.view_args.get('sport_type')
    logger.debug(f"Cache key for sport type: {sport_type}")
    return f"sport_stream_{sport_type}"


def post_cache_key():
    json_data = request.get_json(silent=True) or {}
    json_string = json.dumps(json_data, sort_keys=True)
    hashed_key = hashlib.md5(json_string.encode('utf-8')).hexdigest()
    logger.debug(f"Generated cache key: {hashed_key} for method {request.method} on path {request.path}")
    return f"{request.method}:{request.path}:{hashed_key}"


def check_positive_param(param_name):
    param_value = request.args.get(param_name, type=int)
    if param_value is None or param_value <= 0:
        logger.warning(f"Invalid parameter value for {param_name}: {param_value}")
        return False
    logger.debug(f"Valid parameter value for {param_name}: {param_value}")
    return True
