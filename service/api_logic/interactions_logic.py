from exept.exeptions import UndefinedInteractionType
from enum import Enum

class InteractionTypes(Enum):
    UNDEFINED = 0
    LIKE = 1
    DISLIKE = 2
    READ = 3
    OPEN = 4
    COMMENT = 5

def get_interaction_type_id(interaction_type_name: str) -> int:
    match interaction_type_name:
        case 'like':
            return InteractionTypes.LIKE.value
        case 'dislike':
            return InteractionTypes.DISLIKE.value
        case 'read':
            return InteractionTypes.READ.value
        case 'open':
            return InteractionTypes.OPEN.value
        case 'comment':
            return InteractionTypes.COMMENT.value
        case _:
            return InteractionTypes.UNDEFINED.value

class InteractionWithNewsService:

    def __init__(self, interaction_with_news_dal):
        self._interaction_with_news_dal = interaction_with_news_dal

    def save_interaction(self, interaction_dto):
        interaction_type_id = get_interaction_type_id(interaction_dto.interaction_type)
        if interaction_type_id == InteractionTypes.UNDEFINED.value:
            raise UndefinedInteractionType(interaction_dto.interaction_type)

        return self._interaction_with_news_dal.save_interaction(interaction_dto, interaction_type_id)


    def get_interaction_status(self, interaction_dto):
        interaction_type_id = get_interaction_type_id(interaction_dto.interaction_type)
        if interaction_type_id == InteractionTypes.UNDEFINED.value:
            raise UndefinedInteractionType(interaction_dto.interaction_type)

        interaction_entry = self._interaction_with_news_dal.get_interaction_by_user_id_and_news_id_and_type(interaction_dto.user_id,
                                                                                interaction_dto.news_id,
                                                                                interaction_type_id)
        if interaction_entry:
            return {"status": True}, 200
        return {"status": False}, 404
