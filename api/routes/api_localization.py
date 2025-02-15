from flask import Blueprint, request, make_response, jsonify, flash, current_app

from dto.api_output import get_script_phrases
from exept.exeptions import CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from flask_babel import Babel

babel = Babel()

logger = Logger("logger", "all.log")
localization_app = Blueprint('localization', __name__)

LANGUAGES = ['en', 'uk']

def get_locale():
    return request.cookies.get('lang') or request.accept_languages.best_match(LANGUAGES)


@localization_app.route('/localization', methods=['GET'])
@handle_exceptions
@logger.log_function_call()
def localization():
    try:
        script_phrases = get_script_phrases()

        return script_phrases

    except CustomQSportException as e:
        logger.error(f"Error in GET /localization: {str(e)}")
        return get_custom_error_response(e)


@localization_app.route('/set_language/<language>', methods=['GET'])
@handle_exceptions
@logger.log_function_call()
def set_language(language):
    try:
        response = make_response(jsonify({"message": f"Language set to {language}"}))
        response.set_cookie('lang', language)

        return response

    except CustomQSportException as e:
        logger.error(f"Error in GET /set_language: {str(e)}")
        return get_custom_error_response(e)