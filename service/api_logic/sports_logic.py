from database.models import Sport
from database.session import SessionLocal

session = SessionLocal()

def get_all_sports():
    sports = session.query(Sport).all()
    if not sports:
        print("\033[31mNo sports found in the database.\033[0m")
        return []
    return [
        {
        "sport_id": sport.sport_id,
             "sport_name": sport.sport_name
        } for sport in sports]