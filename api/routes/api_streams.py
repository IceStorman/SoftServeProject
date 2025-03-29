from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request
from api.container.container import Container
from database.postgres.dto import StreamDTO
from dto.api_input import SearchDTO
from exept.exeptions import CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from service.api_logic.streams_logic import StreamService


logger = Logger("logger", "all.log")

streams_app = Blueprint('streams_app', __name__)


@streams_app.route('/search', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def get_filtered_streams_endpoint(streams_service: StreamService = Provide[Container.stream_service]):
    try:
        data = request.get_json()
        dto = SearchDTO().load(data)
        response = streams_service.get_streams_filtered(dto)

        return response

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)