from flask import Blueprint, request
from dto.api_input import UpdateUserPreferencesDTO, GetUserPreferencesDTO
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from dependency_injector.wiring import inject, Provide
from service.api_logic.user_logic import UserService
from api.container.container import Container



api_routes_logger = Logger("api_routes_logger", "api_routes_logger.log")

preferences_app = Blueprint('preferences_app', __name__)


@preferences_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}

    return response


@preferences_app.route('/', methods=['POST', 'DELETE'])
@inject
@handle_exceptions
@api_routes_logger.log_function_call()
def sport_preferences_endpoint(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = UpdateUserPreferencesDTO().load(data)

        if request.method == "POST":
            result = service.add_preferences(dto)

            return result

        if request.method == "DELETE":
            result = service.delete_preferences(dto)

            return result

    except CustomQSportException as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)


@preferences_app.route('/get', methods=['POST'])
@inject
@handle_exceptions
@api_routes_logger.log_function_call()
def get_user_sport_preferences_endpoint(service: UserService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = GetUserPreferencesDTO().load(data)
        result = service.get_user_preferences(dto)

        return result

    except CustomQSportException as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)


@preferences_app.route('/all', methods=['GET'])
@inject
@handle_exceptions
@api_routes_logger.log_function_call()
def get_all_sport_preferences_endpoint(service: UserService = Provide[Container.user_service]):
    try:
        result = service.get_all_preferences()

        return result

    except CustomQSportException as e:
        api_routes_logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)