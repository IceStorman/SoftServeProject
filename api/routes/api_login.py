from flask import Blueprint, jsonify, request
from tensorflow.python.ops.initializers_ns import identity

from dto.api_input import InputUserDTO, ResetPasswordDTO, NewPasswordDTO, InputUserLoginDTO
from dto.common_responce import CommonResponseWithUser
from exept.exeptions import DatabaseConnectionError, SoftServeException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from dependency_injector.wiring import inject, Provide
from service.api_logic.user_logic import UserService
from api.container.container import Container
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from datetime import timedelta


logger = Logger("logger", "all.log")

login_app = Blueprint('login_app', __name__)


@login_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@login_app.route('/sign_up', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def create_account_endpoint(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = InputUserDTO().load(data)
        result = service.create_user(dto.email, dto.username, dto.password_hash)

        return result

    except SoftServeException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)


@login_app.route('/reset-password-request', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def request_password_reset(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = ResetPasswordDTO().load(data)
        result = service.request_password_reset(dto.email)

        return result

    except SoftServeException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)

@login_app.route('/reset-password/<token>', methods=['GET', 'POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def reset_password(token, service: UserService = Provide[Container.user_service]):
    try:
        if request.method == "GET":
            user_data = service.confirm_token(token)

            return user_data

        if request.method == "POST":
            data = request.get_json()
            dto = NewPasswordDTO().load(data)
            token = service.reset_user_password(dto.email, dto.new_password)

            return token

    except SoftServeException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)

@login_app.route('/login', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def log_in(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = InputUserLoginDTO().load(data)
        user = service.log_in(dto.email_or_username, dto.password_hash)
        access_token = create_access_token(identity=user.email)

        response = CommonResponseWithUser(user_id=user.id, user_email=user.email).to_dict()
        response_json = jsonify(response)

        set_access_cookies(response_json, access_token)

        return response_json

    except SoftServeException as e:
        logger.error(f"Error in POST /login: {str(e)}")
        return get_custom_error_response(e)



