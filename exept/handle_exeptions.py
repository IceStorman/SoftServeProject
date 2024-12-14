from functools import wraps
from sqlalchemy.exc import OperationalError
from exept.exeptions import SoftServeException, DatabaseConnectionError
from api.routes.scripts import get_error_response

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except OperationalError:
            raise DatabaseConnectionError
        except SoftServeException as e:
            return e.get_response()
        except Exception as e:
            response = {"error in service": str(e)}
            return get_error_response(response, 500)
        return result

    return wrapper


