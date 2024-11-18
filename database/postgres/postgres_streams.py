from sqlalchemy.orm import Session
from ..models import Stream


def create_stream(db: Session,
                stream_url: str,
                start_time: int,
                status: bool,
                sport_id:int):
    db_stream = Stream(stream_url=stream_url,
                            start_time=start_time,
                            status=status,
                            sport_id=sport_id
                              )
    db.add(db_stream)
    db.commit()
    db.refresh(db_stream)
    return db_stream
