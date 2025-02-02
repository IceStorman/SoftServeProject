import functools
from functools import wraps

import asyncio
from flask import jsonify
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError
from sqlalchemy.util import await_only
from tensorflow.python.eager.context import async_wait

from exept.exeptions import SoftServeException, DatabaseConnectionError


def handle_exceptions(func):
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                foo = await func(*args, **kwargs)
                return foo
            except OperationalError:
                raise DatabaseConnectionError
            except ValidationError as e:
                return get_custom_error_response(e)
            except Exception as e:
                return get_exception_error_response(e)

        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except OperationalError:
                raise DatabaseConnectionError
            except ValidationError as e:
                return get_custom_error_response(e)
            except Exception as e:
                return get_exception_error_response(e)

        return sync_wrapper


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






