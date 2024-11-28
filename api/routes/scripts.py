from flask import jsonify, request


def get_error_response(e, status_code):
    return jsonify(e), status_code


def make_cache_key():
   sport_type = request.view_args.get('sport_type')
   return f"sport_stream_{sport_type}"
