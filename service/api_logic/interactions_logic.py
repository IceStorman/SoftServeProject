from exept.exeptions import IncorrectInteractionType
from service.api_logic.models.api_models import InteractionTypes
from logger.logger import Logger

LIKE_ID = InteractionTypes['LIKE'].value
DISLIKE_ID = InteractionTypes['DISLIKE'].value

class InteractionWithNewsService:

    def __init__(self, interaction_with_news_dal):
        self._interaction_with_news_dal = interaction_with_news_dal
        self._logger = Logger("logger", "all.log").logger


    def save_interaction(self, interaction_dto):
        try:
            interaction_type_id = InteractionTypes[interaction_dto.interaction_type.upper()].value

            if interaction_type_id == LIKE_ID:
                interaction_entry = self._interaction_with_news_dal.get_interaction(interaction_dto.user_id, interaction_dto.news_id, DISLIKE_ID)

                if interaction_entry:
                    self._interaction_with_news_dal.update_interaction(interaction_entry.user_id, interaction_dto, interaction_type_id)
                else:
                    self._interaction_with_news_dal.save_interaction(interaction_dto, interaction_type_id)

            elif interaction_type_id == DISLIKE_ID:
                interaction_entry = self._interaction_with_news_dal.get_interaction(interaction_dto.user_id, interaction_dto.news_id, LIKE_ID)

                if interaction_entry:
                    self._interaction_with_news_dal.update_interaction(interaction_entry.user_id, interaction_dto, interaction_type_id)

            else:
                self._interaction_with_news_dal.save_interaction(interaction_dto, interaction_type_id)

        except KeyError:
            raise IncorrectInteractionType()


    def get_interaction_status(self, interaction_dto) -> bool:
        try:
            interaction_id = InteractionTypes[interaction_dto.interaction_type.upper()].value
            interaction_entry = self._interaction_with_news_dal.get_interaction(interaction_dto.user_id, interaction_dto.news_id, interaction_id)

            return True if interaction_entry else False

        except KeyError:
            raise IncorrectInteractionType()