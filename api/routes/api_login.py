from accelerate.commands.config.update import description
from flask import request, current_app, redirect, jsonify
from oauthlib.oauth2 import WebApplicationClient
from flask_smorest import Blueprint
from dto.api_input import InputUserDTO, InputUserByEmailDTO, NewPasswordDTO, InputUserLogInDTO
from dto.api_output import OutputLogin
from dto.common_response import CommonResponse
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from dependency_injector.wiring import inject, Provide
from service.api_logic.user_logic import UserService
from api.container.container import Container
from flask_jwt_extended import jwt_required
import os
from dotenv import load_dotenv

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
load_dotenv()
FRONT_RESET_PASSWORD_URL = os.getenv('FRONT_RESET_PASSWORD_URL')

logger = Logger("logger", "all.log")

login_app = Blueprint('login_app', __name__, description="Login options", url_prefix='/login')


@login_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@login_app.route('/sign-up', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
@login_app.arguments(InputUserDTO)
@login_app.response(200, CommonResponse().to_dict())
async def create_account_endpoint(service: UserService = Provide[Container.user_service]):
    """Create user account"""
    try:
        data = request.get_json()
        dto = InputUserDTO().load(data)
        response = await service.sign_up_user(dto.email, dto.username, dto.password)

        return response

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)



@login_app.route('/reset-password-request', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
@login_app.arguments(InputUserByEmailDTO)
@login_app.response(200, CommonResponse().to_dict())
def request_password_reset(dto: InputUserByEmailDTO, service: UserService = Provide[Container.user_service]):
    """Send request to change password"""
    try:
        result = service.request_password_reset(dto.email)

        return jsonify(result)

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)


@login_app.route('/reset-password/<token>', methods=['GET', 'POST'])
@inject
@handle_exceptions
@logger.log_function_call()
@login_app.arguments(NewPasswordDTO)
@login_app.response(200, CommonResponse().to_dict())
@login_app.response(302)
def reset_password(dto: NewPasswordDTO, token, service: UserService = Provide[Container.user_service]):
    """
       Reset password functionality.

       **GET** request: Redirects to front-end reset password page.

       **POST** request: Accepts the new password and resets it.
    """
    try:
        if request.method == "GET":
            user = service.confirm_token(token)

            reset_front_url = f"{FRONT_RESET_PASSWORD_URL}/{token}"

            return redirect(reset_front_url)

        if request.method == "POST":
            token = service.reset_user_password(token, dto.password)

            return token

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)


@login_app.route('/login', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
@login_app.arguments(InputUserLogInDTO)
@login_app.response(200, CommonResponse().to_dict())
async def log_in(dto: InputUserLogInDTO, service: UserService = Provide[Container.user_service]):
    """Log in to account"""
    try:
        response = await service.log_in(dto)

        return response

    except CustomQSportException as e:
        logger.error(f"Error in POST /login: {str(e)}")
        return get_custom_error_response(e)

@login_app.route("/refresh", methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
@jwt_required(refresh=True)
async def refresh(service: UserService = Provide[Container.user_service]):
    try:
        return await service.refresh_tokens()
    except CustomQSportException as e:
        logger.error(f"Error in POST /refresh: {str(e)}")
        return get_custom_error_response(e)