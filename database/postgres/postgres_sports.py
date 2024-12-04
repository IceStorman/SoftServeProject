from sqlalchemy.orm import Session
from ..models import Sport


def create_sport(db: Session,
                sport_name: str):
    db_sport = Sport(sport_name=sport_name)
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    return db_sport
