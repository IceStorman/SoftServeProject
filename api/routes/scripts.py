from flask import jsonify, request


def get_error_response(e, status_code):
    return jsonify(e), status_code


def make_cache_key():
   sport_type = request.view_args.get('sport_type')
   return f"sport_stream_{sport_type}"


def check_positive_param(param_name):
    param_value = request.args.get(param_name, type=int)
    if param_value is None or param_value <= 0:
        return False
    return True
