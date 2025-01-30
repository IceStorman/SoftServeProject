from functools import wraps
from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError
from exept.exeptions import SoftServeException, DatabaseConnectionError


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except OperationalError:
            raise DatabaseConnectionError
        except SoftServeException as e:
            return e.get_response()
        except ValidationError as e:
            get_error_response(e)
        except Exception as e:
            get_error_response(e)

    return wrapper


def get_error_response(e):
    response = {"error in service": str(e)}
    return jsonify(response)






