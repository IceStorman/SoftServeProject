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
        except ValidationError as e:
            return get_custom_error_response(e)
        except Exception as e:
            return get_exception_error_response(e)

    return wrapper


def handle_exceptions_for_class(cls):
    for attr_name in dir(cls):
        if not attr_name.startswith("__"):
            attr = getattr(cls, attr_name)
            if callable(attr) and not isinstance(attr, type):
                setattr(cls, attr_name, handle_exceptions(attr))
    return cls

def get_custom_error_response(e):
    response = {"error": str(e)}
    return jsonify(response), e.status_code

def get_exception_error_response(e):
    response = {"error in service": str(e)}
    return jsonify(response), 500






