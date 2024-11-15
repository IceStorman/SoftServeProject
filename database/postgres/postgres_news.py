from datetime import datetime

from sqlalchemy.orm import Session
from ..models import News


def create_news(db: Session,
                blob_id: int,
                interest_rate: int,
                save_at: datetime):
    db_news = News(blob_id=blob_id,
                   interest_rate=interest_rate,
                   save_at=save_at)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news
