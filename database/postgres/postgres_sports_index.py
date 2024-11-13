from sqlalchemy.orm import Session
from ..models import SportIndex


def create_sport_index(db: Session,
                sport_id: int):
    db_sport_index = SportIndex(sport_id=sport_id)
    db.add(db_sport_index)
    db.commit()
    db.refresh(db_sport_index)
    return db_sport_index
