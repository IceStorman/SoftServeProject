from functools import wraps
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError
from exept.exeptions import SoftServeException, DatabaseConnectionError
from api.routes.scripts import get_error_response

def code_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except OperationalError:
            raise DatabaseConnectionError
        except SoftServeException as e:
            return e.get_response()
        except ValidationError as e:
            response = {"error in validation": str(e)}
            return get_error_response(response, 400)
        except Exception as e:
            response = {"error in service": str(e)}
            return get_error_response(response, 500)
        return result, 200

    return wrapper


