from database.postgres.dal.base import BaseDAL
from sqlalchemy.orm import Session
from sqlalchemy import ClauseElement
from database.models import Comment
from datetime import datetime

class CommentDAL(BaseDAL):
    def __init__(self, session: Session):
        self.db_session = session

    def create_comment(self, comment_dto):
        new_comment = Comment(
            user_id=comment_dto.user_id,
            news_id=comment_dto.news_id,
            timestamp=datetime.now(),
            content=comment_dto.content,
            parent_comment_id=comment_dto.parent_comment_id
        )
        self.db_session.add(new_comment)
        self.db_session.commit()

    def update_comment(self, comment_id, comment_dto):
        self.db_session.query(Comment).filter(Comment.comment_id == comment_id).update(
            {"content":comment_dto.content}
        )
        self.db_session.commit()

    def fetch_comments(self, comment_dto, order_by=None):
        query = self.db_session.query(Comment)

        query = query.filter(Comment.news_id == comment_dto.news_id,
                             Comment.parent_comment_id == comment_dto.parent_comment_id)


        if order_by is not None:
            if isinstance(order_by, ClauseElement):
                query = query.order_by(order_by)
            else:
                raise ValueError("Invalid order_by argument. Must be a SQLAlchemy ClauseElement.")

        return query.all()


    def get_comment_bt_id(self, comment_id):
        return self.db_session.query(Comment).filter_by(comment_id=comment_id).first()

    def delete_comment(self, comment_id):
        comment_entry = self.get_comment_bt_id(comment_id)
        self.db_session.delete(comment_entry)
        self.db_session.commit()
