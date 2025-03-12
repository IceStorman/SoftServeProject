from flask import Blueprint, request
from dto.api_input import InteractionsDTO
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response
from logger.logger import Logger
from service.api_logic.interactions_logic import save_interaction, get_interaction_status

logger = Logger("logger", "all.log")

interactions_app = Blueprint('interactions', __name__)

@interactions_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response

@interactions_app.route('/save', methods=['POST'])
@logger.log_function_call()
def save_interaction():
    try:
        data = request.get_json()
        dto = InteractionsDTO().load(data)
        save_interaction(dto)

        return {"message": "Interaction added successfully"}, 201
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)

@interactions_app.route('/getStatus', methods=['GET'])
@logger.log_function_call()
def get_interaction_status_by_user_id():
    try:
        user_id = request.args.get("user_id")
        news_id = request.args.get("news_id")
        interaction_type = request.args.get("interaction_type")
        dto = InteractionsDTO.load({"news_id": news_id, "user_id": user_id, "interaction_type": interaction_type})
        status = get_interaction_status(dto)

        return {"status": status}, 200
    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)
