from exept.exeptions import IncorrectInteractionType
from service.api_logic.models.api_models import InteractionTypes
from database.postgres.dto import InteractionWithNewsDTO
from logger.logger import Logger

LIKE_ID = InteractionTypes['LIKE'].value
DISLIKE_ID = InteractionTypes['DISLIKE'].value

class InteractionWithNewsService:

    def __init__(self, interaction_with_news_dal, news_dal):
        self._interaction_with_news_dal = interaction_with_news_dal
        self._logger = Logger("logger", "all.log").logger
        self._news_dal = news_dal


    def _convert_input_to_db_dto(self, interaction_input_dto):
        interaction_type_id = InteractionTypes[interaction_input_dto.interaction_type.upper()].value
        news_id = self._news_dal.get_news_by_id(interaction_input_dto.blob_id).news_id

        if not news_id or not interaction_type_id:
            raise ValueError

        db_dto = InteractionWithNewsDTO(
            news_id=news_id,
            user_id=interaction_input_dto.user_id,
            interaction_type=interaction_type_id,
            timestamp=interaction_input_dto.timestamp,
        )

        return db_dto


    def save_interaction(self, interaction_input_dto):
        try:
            interaction_dto = self._convert_input_to_db_dto(interaction_input_dto)

            if interaction_dto.interaction_type == LIKE_ID:
                interaction_entry = self._interaction_with_news_dal.get_interaction(interaction_dto.user_id, interaction_dto.news_id, DISLIKE_ID)

                if interaction_entry:
                    self._interaction_with_news_dal.update_interaction(interaction_entry.interaction_id, interaction_dto)
                else:
                    self._interaction_with_news_dal.save_interaction(interaction_dto)

            elif interaction_dto.interaction_type == DISLIKE_ID:
                interaction_entry = self._interaction_with_news_dal.get_interaction(interaction_dto.user_id, interaction_dto.news_id, LIKE_ID)

                if interaction_entry:
                    self._interaction_with_news_dal.update_interaction(interaction_entry.interaction_id, interaction_dto)

            else:
                self._interaction_with_news_dal.save_interaction(interaction_dto)

        except KeyError:
            raise IncorrectInteractionType()


    def get_interaction_status(self, interaction_input_dto) -> bool:
        try:
            interaction_dto = self._convert_input_to_db_dto(interaction_input_dto)
            interaction_entry = self._interaction_with_news_dal.get_interaction(interaction_dto.user_id, interaction_dto.news_id, interaction_dto.interaction_type)

            return True if interaction_entry else False

        except KeyError:
            raise IncorrectInteractionType()