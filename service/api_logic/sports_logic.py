from database.models import Sport
from exept.colors_text import print_error_message
from exept.exeptions import DatabaseConnectionError
from sqlalchemy.exc import OperationalError

def get_all_sports(session):
    try:
        sports = session.query(Sport).all()
        if not sports:
            print_error_message("No sports found in the database")
            return [], 204
        return [
            {
                "sport_id": sport.sport_id,
                "sport_name": sport.sport_name,
                "sport_img": sport.sport_img
            } for sport in sports], 200
    except OperationalError:
        raise DatabaseConnectionError()
    except Exception as e:
        raise Exception (f"An unexpected error occurred: {str(e)}") from e
