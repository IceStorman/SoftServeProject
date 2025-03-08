import datetime

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request
from api.container.container import Container
from database.postgres.dto import StreamDTO
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
def get_all_streams_endpoint(streams_service: StreamService = Provide[Container.stream_service]): #I guess this will be temporary endpoint, as filters will cover most of our needs
    try:
        # dto = StreamDTO(
        #     stream_url = ["https://github.com/IceStorman/SoftServeProject/pulls", "https://example.com/stream2"],
        #     start_time = datetime.datetime(2025, 3, 8),
        #     sport_id = 1
        # )
        # streams_service._stream_dal.create_stream(dto)
        response = streams_service.all_streams()
        return response

    except CustomQSportException as e:
        logger.error(f"Error in Get /: {str(e)}")
        return get_custom_error_response(e)


@streams_app.route('/filtered', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def get_filtered_streams_endpoint(streams_service: StreamService = Provide[Container.stream_service]):
    try:
        data = request.get_json()
        dto = StreamDTO().load(data)
        response = streams_service.get_streams_filtered(dto)
        return response

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)