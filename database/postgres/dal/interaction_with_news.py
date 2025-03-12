from sqlalchemy.orm import Session
from database.models import InteractionWithNews
from typing import Optional

LIKE_RELATED_INTERACTIONS_SPAN = [1, 2]

class InteractionWithNewsDAL:
    def __init__(self, db_session: Session = None):
        self.db_session = db_session
        
    def save_interaction(self, interaction_dto, interaction_type_id: int):
        interaction_type_id_search_option = interaction_type_id
        if interaction_type_id in LIKE_RELATED_INTERACTIONS_SPAN:
            interaction_type_id_search_option = sum(LIKE_RELATED_INTERACTIONS_SPAN) - interaction_type_id
        interaction_entry = self.get_interaction_by_user_id_and_news_id_and_type(interaction_dto.user_id,
                                                                                 interaction_dto.news_id,
                                                                                 interaction_type_id_search_option)
        if interaction_entry:
            self.update_interaction(interaction_entry.interaction_id, interaction_dto, interaction_type_id)
            return {"message": "Interaction was updated"}, 200
        else:
            self.create_interaction(interaction_dto, interaction_type_id)
            return {"message": "Interaction was created"}, 201
    
    def create_interaction(self, interaction_dto, interaction_type_id: int) -> InteractionWithNews:
        new_interaction = InteractionWithNews(
            news_id=interaction_dto.news_id,
            user_id=interaction_dto.user_id,
            interaction_type=interaction_type_id,
            timestamp=interaction_dto.timestamp
        )
        self.db_session.add(new_interaction)
        self.db_session.commit()
        return new_interaction

    def update_interaction(self, interaction_id: int, interaction_dto, interaction_type_id: int) -> Optional[InteractionWithNews]:
        interaction = self.get_interaction_by_id(interaction_id)
        if not interaction:
            return None
        setattr(interaction, 'timestamp', interaction_dto.timestamp)
        setattr(interaction, 'interaction_type', interaction_type_id)
        self.db_session.commit()
        self.db_session.refresh(interaction)
        return interaction

    def get_interaction_by_user_id_and_type(self, user_id: int, interaction_type_id: int) -> Optional[InteractionWithNews]:
        return self.db_session.query(InteractionWithNews).filter_by(user_id=user_id).filter_by(interaction_type=interaction_type_id).first()

    def get_interaction_by_user_id_and_news_id_and_type(self, user_id: int, news_id: int, interaction_type_id: int) -> Optional[InteractionWithNews]:
        return self.db_session.query(InteractionWithNews).filter_by(user_id=user_id).filter_by(news_id=news_id).filter_by(interaction_type=interaction_type_id).first()

    def get_interaction_by_id(self, interaction_id: int) -> Optional[InteractionWithNews]:
        return self.db_session.query(InteractionWithNews).filter_by(interaction_id=interaction_id).first()

    def delete_interaction(self, interaction_id: int) -> bool:
        interaction = self.get_interaction_by_id(interaction_id)
        if not interaction:
            return False
        self.db_session.delete(interaction)
        self.db_session.commit()
        return True