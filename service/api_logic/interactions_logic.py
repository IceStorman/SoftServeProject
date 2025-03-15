from exept.exeptions import IncorrectInteractionType, BlobFetchError, DatabaseConnectionError
from service.api_logic.models.api_models import InteractionTypes
from database.postgres.dto import InteractionWithNewsDTO
from logger.logger import Logger
from datetime import datetime

LIKE_ID = InteractionTypes['LIKE'].value
DISLIKE_ID = InteractionTypes['DISLIKE'].value

class InteractionWithNewsService:
    def __init__(self, interaction_with_news_dal, news_dal):
        self._interaction_with_news_dal = interaction_with_news_dal
        self._logger = Logger("logger", "all.log").logger
        self._news_dal = news_dal


    def __convert_input_to_db_dto(self, interaction_input_dto):
        try:
            interaction_type_id = InteractionTypes[interaction_input_dto.interaction_type.upper()].value
            news_entry = self._news_dal.get_news_by_id(interaction_input_dto.blob_id)

            if not news_entry:
                raise BlobFetchError(interaction_input_dto.blob_id)

            db_dto = InteractionWithNewsDTO(
                news_id=news_entry.news_id,
                user_id=interaction_input_dto.user_id,
                interaction_type=interaction_type_id,
                timestamp=datetime.now()
            )

            return db_dto

        except KeyError:
            raise IncorrectInteractionType(interaction_input_dto.interaction_type)


    def save_interaction(self, interaction_input_dto):
        interaction_dto = self.__convert_input_to_db_dto(interaction_input_dto)

        opposite_interaction = {
            LIKE_ID: DISLIKE_ID,
            DISLIKE_ID: LIKE_ID
        }.get(interaction_dto.interaction_type)

        if opposite_interaction:
            interaction_entry = self._interaction_with_news_dal.get_interaction(
                interaction_dto.user_id, interaction_dto.news_id, opposite_interaction
            )

            if interaction_entry:
                self._interaction_with_news_dal.update_interaction(interaction_entry.interaction_id, interaction_dto)
                return

        self._interaction_with_news_dal.save_interaction(interaction_dto)


    def get_interaction_status(self, interaction_input_dto) -> bool:
        interaction_dto = self.__convert_input_to_db_dto(interaction_input_dto)
        interaction_entry = self._interaction_with_news_dal.get_interaction(interaction_dto.user_id, interaction_dto.news_id, interaction_dto.interaction_type)

        return True if interaction_entry else False