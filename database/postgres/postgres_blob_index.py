from sqlalchemy.orm import Session
from ..models import BlobIndex


def create_blob_index(db: Session,
                sports_index_id: int,
                filename: str):
    db_blob_index = BlobIndex(sports_index_id=sports_index_id,
                   filename=filename)
    db.add(db_blob_index)
    db.commit()
    db.refresh(db_blob_index)
    return db_blob_index
