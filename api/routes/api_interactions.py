from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify
from dto.api_input import InteractionsDTO
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from service.api_logic.interactions_logic import InteractionWithNewsService
from api.container.container import Container
from dto.common_response import CommonResponse
from service.api_logic.models.api_models import InteractionTypes
from api.routes.cache import cache

logger = Logger("logger", "all.log")

interactions_app = Blueprint('interactions', __name__)

@interactions_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response

@interactions_app.route('', methods=['POST'])
@logger.log_function_call()
@inject
@handle_exceptions
def save_interaction(service: InteractionWithNewsService = Provide[Container.interaction_with_news_service]):
    try:
        data = request.get_json()
        dto = InteractionsDTO().load(data)
        service.save_interaction(dto)

        return CommonResponse().to_dict()

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)

@interactions_app.route('/status', methods=['GET'])
@logger.log_function_call()
@inject
@handle_exceptions
def get_interaction_status_by_user_id(service: InteractionWithNewsService = Provide[Container.interaction_with_news_service]):
    try:
        dto = InteractionsDTO().load(request.args)
        interaction_status = service.has_interaction_occurred(dto)

        return jsonify(interaction_status)

    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        return get_custom_error_response(e)


@interactions_app.route('/counts', methods=['GET'])
@logger.log_function_call()
@inject
@handle_exceptions
def get_interactions_count_by_blob_id(service: InteractionWithNewsService = Provide[Container.interaction_with_news_service]):
    try:
        dto = InteractionsDTO().load(request.args)
        interactions_counts = service.get_interactions_counts(dto)

        return interactions_counts

    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        return get_custom_error_response(e)


@interactions_app.route('/types', methods=['GET'])
@logger.log_function_call()
@cache.cached(timeout=60*60)
@inject
@handle_exceptions
def get_interaction_types():
    try:
        return jsonify({interaction.name: interaction.value for interaction in InteractionTypes})

    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        return get_custom_error_response(e)