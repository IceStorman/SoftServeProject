from dto.api_output import OutPutUser
from database.models import User
from exept.handle_exeptions import handle_exceptions
from logger.logger import Logger

api_logic_logger = Logger("api_logic_logger", "api_logic_logger.log")

@handle_exceptions
@api_logic_logger.log_function_call()
class UserService:
    def __init__(self, user_dal):
        self.user_dal = user_dal

    def create_user(self, email_front, username_front, password_front):
        existing_user = self.user_dal.get_user_by_email_or_username(email_front, username_front)
        if existing_user:
            return OutPutUser().dump(existing_user)

        new_user = User(email=email_front, username=username_front, password_hash=password_front)
        self.user_dal.create_user(new_user)

        return OutPutUser().dump(new_user)