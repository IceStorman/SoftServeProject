from sqlalchemy.orm import Session
from ..models import ClubPreference


def create_club_pref(db: Session,
                users_id: int,
                preferences: str):
    db_club_pref = ClubPreference(users_id=users_id,
                   preferences=preferences)
    db.add(db_club_pref)
    db.commit()
    db.refresh(db_club_pref)
    return db_club_pref
