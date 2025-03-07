from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request
from api.container.container import Container
from dto.api_input import StreamsDTO
from exept.exeptions import CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from service.api_logic.streams_logic import StreamService

logger = Logger("logger", "all.log")

streams_app = Blueprint('streams_app', __name__)

@streams_app.route('/all', methods=['GET'])
@inject
@handle_exceptions
@logger.log_function_call()
def get_streams_endpoint(streams_service: StreamService = Provide[Container.user_service]): #I guess this will be temporary endpoint, as filters will cover most of our needs
    try:
        response = streams_service.all_streams()
        return response

    except CustomQSportException as e:
        logger.error(f"Error in Get /: {str(e)}")
        return get_custom_error_response(e)


@streams_app.route('/filtered', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def get_streams_endpoint(streams_service: StreamService = Provide[Container.user_service]):
    try:
        data = request.get_json()
        dto = StreamsDTO().load(data)
        response = streams_service.get_streams_filtered(dto)
        return response

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)