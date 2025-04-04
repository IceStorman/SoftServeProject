from database.postgres.dal.base import BaseDAL
from sqlalchemy.orm import Session
from database.models import Comment
from datetime import datetime

class CommentDAL(BaseDAL):
    def __init__(self, session: Session):
        self.session = session

    def create_comment(self, comment_dto):
        new_comment = Comment(
            user_id=comment_dto.user_id,
            news_id=comment_dto.news_id,
            timestamp=datetime.now(),
            content=comment_dto.content,
            parent_comment_id=comment_dto.parent_comment_id
        )
        self.session.add(new_comment)
        self.session.commit()

    def update_comment(self, comment_id, comment_dto):
        self.session.query(Comment).filter(Comment.comment_id == comment_id).update(
            {"content":comment_dto.content}
        )
        self.session.commit()

    def get_comment_bt_id(self, comment_id):
        return self.session.query(Comment).filter_by(comment_id=comment_id).first()

    def delete_comment(self, comment_id):
        comment_entry = self.get_comment_bt_id(comment_id)
        self.session.delete(comment_entry)
        self.session.commit()
