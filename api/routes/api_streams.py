from flask import Blueprint

from logger.logger import Logger
from service.api_logic.streams_logic import get_available_streams

logger = Logger("logger", "all.log")

streams_app = Blueprint('streams_app', __name__)

@streams_app.route('/available', methods=['GET'])
@logger.log_function_call()
def get_streams_endpoint():
    return get_available_streams()