from flask import Blueprint, jsonify, request
from dto.api_input import InputUserDTO, ResetPasswordDTO, NewPasswordDTO, InputUserLoginDTO
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response, get_error_reset_password
from logger.logger import Logger
from dependency_injector.wiring import inject, Provide
from service.api_logic.user_logic import UserService
from api.container.container import Container
from flask_jwt_extended import JWTManager,create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import timedelta


api_routes_logger = Logger("api_routes_logger", "api_routes_logger.log")

login_app = Blueprint('login_app', __name__)


@login_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@login_app.route('/sign_up', methods=['POST'])
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

@login_app.route('/reset-password/<token>', methods=['GET', 'POST'])
@inject
@api_routes_logger.log_function_call()
def reset_password(token, service: UserService = Provide[Container.user_service]):
    try:
        if request.method == "GET":
            user_data = service.confirm_token(token)
            if not user_data:
                return get_error_reset_password()
            return user_data

        if request.method == "POST":
            data = request.get_json()
            dto = NewPasswordDTO().load(data)
            token = service.reset_user_password(dto["email"], dto["new_password"])

            # user = service.user.get_user_by_email(dto["email"])
            # if user:
            #     new_jwt = create_access_token(identity=user.email)
            #     return jsonify({"msg": "Пароль змінено успішно", "token": new_jwt})

            return token

    except Exception as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        return get_error_response(e)

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
            return {"error": "It is necessary to specify email or username and password"}, 400

        user = service.log_in(email_or_username, password)

        if not user:
            return {"error": "Invalid email/username or password"}, 401

        access_token = create_access_token(identity={'id': user.id, 'email': user.email})

        response = {"message": "You successfully loged in!", "user": {"id": user.id, "email": user.email}}
        response_obj = jsonify(response)

        set_access_cookies(response_obj, access_token)

        return response_obj

    except Exception as e:
        api_routes_logger.error(f"Error in POST /login: {str(e)}")
        return get_error_response(e)



