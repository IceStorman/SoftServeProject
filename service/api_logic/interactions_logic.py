from database.postgres.dal import InteractionWithNewsDAL
from database.session import SessionLocal
from enum import Enum

session = SessionLocal()
dal = InteractionWithNewsDAL(session)

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

def save_interaction(interaction_dto):
    interaction_type_id = get_interaction_type_id(interaction_dto.type_of_interaction)
    dal.save_interaction(interaction_dto, interaction_type_id)

def get_interaction_status(interaction_dto) -> bool:
    interaction_entry = dal.get_interaction_by_user_id_and_type(interaction_dto.user_id, interaction_dto.type_of_interaction)
    if interaction_entry:
        return True
    return False
