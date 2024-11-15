from sqlalchemy.orm import Session
from ..models import Interaction


def create_interaction(db: Session,
                user_id: int,
                news_id: int,
                interaction_type: str):
    db_interaction = Interaction(user_id=user_id,
                news_id=news_id,
                interaction_type=interaction_type)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction
