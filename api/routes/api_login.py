from flask import Blueprint, request
from dto.api_input import InputUserDTO, ResetPasswordDTO, NewPasswordDTO, InputUserLoginDTO
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response, get_error_reset_password, get_good_reset_password
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
        dto = InputUserDTO().load(data)

        result = service.create_user(dto["email"], dto["username"], dto["password_hash"])

        return result
    except Exception as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        get_error_response(e)


@login_app.route('/reset-password-request', methods=['POST'])
@inject
@api_routes_logger.log_function_call()
def request_password_reset(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = ResetPasswordDTO().load(data)
        result = service.request_password_reset(dto["email"])
        return result

    except Exception as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        get_error_response(e)

@login_app.route('/reset-password/<token>', methods=['GET','POST'])
@inject
@api_routes_logger.log_function_call()
def reset_password(token, service: UserService = Provide[Container.user_service]):
    try:
        if request.method == "GET":
            user_data = service.confirm_token(token)
            print(user_data)
            if not user_data:
                return get_error_reset_password()
            return user_data

        if request.method == "POST":
            data = request.get_json()
            dto = NewPasswordDTO().load(data)
            service.reset_user_password(dto["email"], dto["new_password"])
            return get_good_reset_password()
    except Exception as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        get_error_response(e)

@login_app.route('/login', methods=['POST'])
@inject
@api_routes_logger.log_function_call()
def log_in(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()

        dto = InputUserLoginDTO().load(data)
        email_or_username = dto['email_or_username']
        password = dto['password_hash']

        if not email_or_username or not password:
            return {"error": "Необхідно вказати email або username і пароль"}, 400

        result = service.log_in(email_or_username, password)
        return result

    except Exception as e:
        api_routes_logger.error(f"Error in POST /login: {str(e)}")
        return get_error_response(e)


