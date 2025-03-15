from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify
from dto.api_input import InteractionsDTO
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from service.api_logic.interactions_logic import InteractionWithNewsService
from api.container.container import Container
from dto.common_response import CommonResponse

logger = Logger("logger", "all.log")

interactions_app = Blueprint('interactions', __name__)

@interactions_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response

@interactions_app.route('/save', methods=['POST'])
@logger.log_function_call()
@inject
@handle_exceptions
def save_interaction(service: InteractionWithNewsService = Provide[Container.interaction_with_news_service]):
    try:
        data = request.get_json()
        dto = InteractionsDTO().load(data)
        service.save_interaction(dto)

        return  CommonResponse().to_dict()

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)

@interactions_app.route('/getStatus', methods=['GET'])
@logger.log_function_call()
@inject
@handle_exceptions
def get_interaction_status_by_user_id(service: InteractionWithNewsService = Provide[Container.interaction_with_news_service]):
    try:
        dto = InteractionsDTO().load(request.args.to_dict())
        response = service.get_interaction_status(dto)

        return jsonify(response)

    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        return get_custom_error_response(e)
