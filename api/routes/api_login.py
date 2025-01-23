from flask import Blueprint, request
from dto.api_input import CreateAccountDTO
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response
from logger.logger import Logger
from dependency_injector.wiring import inject, Provide
from service.api_logic.login_logic import UserService
from api.container.container import Container

api_routes_logger = Logger("api_routes_logger", "api_routes_logger.log")

login_app = Blueprint('login_app', __name__)

@login_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response

@login_app.route('/sing_up', methods=['POST'])
@inject
@api_routes_logger.log_function_call()
def create_account_endpoint(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = CreateAccountDTO().load(data)

        result = service.create_user(dto["email"], dto["username"], dto["password_hash"])

        return result
    except Exception as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        get_error_response(e)