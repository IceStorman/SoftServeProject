from database.models import Comment, User
from database.postgres.dto import CommentDTO
from dto.api_output import OutputComment

from logger.logger import Logger


class CommentsService:
    def __init__(self, comments_dal, news_dal):
        self._logger = Logger("logger", "all.log").logger
        self._comment_dal = comments_dal
        self._news_dal = news_dal

    def __convert_dal(self, input_dal):
        news_entry = self._news_dal.get_news_by_id(input_dal.article_blob_id)

        if not news_entry:
            pass

        db_dto =  CommentDTO(
            comment_id=input_dal.comment_id,
            user_id=input_dal.user_id,
            news_id=news_entry.news_id,
            content=input_dal.content,
            parent_comment_id=input_dal.parent_comment_id
        )

        return db_dto

    def save_comment(self, input_comment_dto):
        comment_dto = self.__convert_dal(input_comment_dto)
        self._comment_dal.create_comment(comment_dto)

    def get_comments(self, input_comment_dto, page: int = 1, per_page: int = 10):
        comment_dto = self.__convert_dal(input_comment_dto)

        query = (self._comment_dal.get_base_query(Comment).with_entities(
            Comment.comment_id,
            Comment.user_id,
            User.username,
            Comment.content,
            Comment.timestamp,
            Comment.parent_comment_id
        )
                 .join(User, User.user_id == Comment.user_id)
                 .filter(
            Comment.news_id == comment_dto.news_id,
            Comment.parent_comment_id == comment_dto.parent_comment_id
        )
                 .order_by(Comment.timestamp.desc())
                 .limit(per_page)
                 .offset((page - 1) * per_page))

        comments = self._comment_dal.query_output(query)
        comment_output = OutputComment(many=True).dump(comments)

        return {
            "comments": comment_output,
            "has_more": len(comments) == per_page
        }

    def edit_comment(self, comment_dto):
        self._comment_dal.update_comment(comment_dto.comment_id, comment_dto)

    def delete_comment(self, comment_dto):
        self._comment_dal.delete_comment(comment_dto.comment_id)