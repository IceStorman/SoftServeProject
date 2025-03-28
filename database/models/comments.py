from .base import Base, Column, Integer, String, ForeignKey, DateTime

class Comment(Base):
    __tablename__ = 'Comments'
    comment_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('Users.user_id'))
    news_id = Column(ForeignKey('News.news_id'))
    timestamp = Column(DateTime(timezone=True))
    content = Column(String(80))
    parent_comment_id = Column(ForeignKey('Comments.comment_id'))
