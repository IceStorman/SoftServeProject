from sqlalchemy.orm import Session
from ..models import User


# тут десь мають використовуватись DTO?
def create_user(db: Session,
                username: str,
                email: str,
                password_hash: str,
                sport_pref_key:int,
                club_pref_key:int,
                theme: str):
    db_user = User(username=username,
                   email=email,
                   password_hash=password_hash,
                   sport_pref_key=sport_pref_key,
                   club_pref_key=club_pref_key,
                   theme=theme)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
