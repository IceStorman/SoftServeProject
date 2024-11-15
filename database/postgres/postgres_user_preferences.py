from sqlalchemy.orm import Session
from ..models import UserPreference


def create_user_pref(db: Session,
                sports_id: int,
                users_id: int):
    db_user_pref = UserPreference(sports_id=sports_id,
                   users_id=users_id)
    db.add(db_user_pref)
    db.commit()
    db.refresh(db_user_pref)
    return db_user_pref
