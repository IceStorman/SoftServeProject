from functools import wraps
from sqlalchemy.exc import OperationalError
from exept.exeptions import DatabaseConnectionError, SoftServeException

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as oe:
            raise DatabaseConnectionError(oe)
        except SoftServeException as e:
            raise SoftServeException from e
    return wrapper