from flask import Blueprint, request, current_app, redirect
from oauthlib.oauth2 import WebApplicationClient
from dto.api_input import InputUserDTO, InputUserByEmailDTO, NewPasswordDTO, InputUserLogInDTO
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from dependency_injector.wiring import inject, Provide
from service.api_logic.user_logic import UserService
from api.container.container import Container
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

logger = Logger("logger", "all.log")

login_app = Blueprint('login_app', __name__)


@login_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@login_app.route('/sign-up', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
async def create_account_endpoint(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = InputUserDTO().load(data)
        user = await service.sign_up_user(dto.email, dto.username, dto.password_hash)
        response = await service.create_access_token_response(user)

        return response

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)



@login_app.route('/reset-password-request', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def request_password_reset(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = InputUserByEmailDTO().load(data)
        result = service.request_password_reset(dto.email)

        return result

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)

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

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)

@login_app.route('/login', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
async def log_in(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = InputUserLogInDTO().load(data)
        response = await service.log_in(dto)

        return response

    except CustomQSportException as e:
        logger.error(f"Error in POST /login: {str(e)}")
        return get_custom_error_response(e)

@login_app.route("/login/google", methods=['GET'])
@inject
@handle_exceptions
@logger.log_function_call()
def login_google():
    try:
        with current_app.app_context():
            client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
            authorization_url = client.prepare_request_uri(
                current_app.config['AUTHORIZATION_BASE_URL'],
                redirect_uri = current_app.config['REDIRECT_URI'],
                scope=current_app.config['SCOPES']
            )

        return redirect(authorization_url)

    except CustomQSportException as e:
        logger.error(f"Error in GET /login/google: {str(e)}")
        return get_custom_error_response(e)
    
@login_app.route("/refresh", methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
@jwt_required(refresh=True)
def refresh(service: UserService = Provide[Container.user_service]):
    identity = get_jwt_identity()   
    return service.create_new_access_token(identity)



