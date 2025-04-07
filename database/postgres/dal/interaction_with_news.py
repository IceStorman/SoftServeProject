from database.models import InteractionWithNews
from typing import Optional


class InteractionWithNewsDAL:
    def __init__(self, db_session = None):
        self.db_session = db_session
    
    def create_interaction(self, interaction_dto):
        new_interaction = InteractionWithNews(
            news_id=interaction_dto.news_id,
            user_id=interaction_dto.user_id,
            interaction_type=interaction_dto.interaction_type,
            timestamp=interaction_dto.timestamp
        )
        self.db_session.add(new_interaction)
        self.db_session.commit()

    def update_interaction(self, interaction_dto, interaction_type_id: int = None) -> bool:
        rows_updated = (self.db_session.query(InteractionWithNews)
            .filter(InteractionWithNews.user_id==interaction_dto.user_id,
                    InteractionWithNews.news_id==interaction_dto.news_id,
                    InteractionWithNews.interaction_type ==
                        (interaction_type_id if interaction_type_id is not None else interaction_dto.interaction_type))
            .update({
                InteractionWithNews.timestamp: interaction_dto.timestamp,
                InteractionWithNews.interaction_type: interaction_dto.interaction_type
            }))
        self.db_session.commit()

        return bool(rows_updated)

    def get_interaction(self, user_id: int, news_id: int, interaction_type_id: int) -> Optional[InteractionWithNews]:
        """
        Retrieves a user's interaction with a news item based on given parameters.

        :param user_id: The ID of the user.
        :param news_id: The ID of the article.
        :param interaction_type_id: The type of interaction.
        :return: An InteractionWithNews object if found, otherwise None.
        """
        return self.db_session.query(InteractionWithNews).filter_by(user_id=user_id, news_id=news_id, interaction_type=interaction_type_id).first()
