from database.models import Sport
from database.session import SessionLocal
from exept.colors_text import print_error_message

session = SessionLocal()

def get_all_sports():
    sports = session.query(Sport).all()
    if not sports:
        print_error_message("No sports found in the database")
        return [], 204
    return [
        {
            "sport_id": sport.sport_id,
            "sport_name": sport.sport_name
        } for sport in sports], 200