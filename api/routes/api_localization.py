import json
from pathlib import Path
from flask import Blueprint, request, jsonify
from dto.api_output import get_script_phrases
from exept.exeptions import CustomQSportException
from exept.handle_exeptions import get_custom_error_response, handle_exceptions
from logger.logger import Logger
from flask_babel import Babel

babel = Babel()

logger = Logger("logger", "all.log")
localization_app = Blueprint('localization', __name__)

LANGUAGES = ['en', 'uk']
VERSION_FILE = "translation_version.json"

def get_locale():
    return request.cookies.get('lang') or request.accept_languages.best_match(LANGUAGES)


def get_translation_version_from_file():
    if Path(VERSION_FILE).exists():
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)

            return data.get("version", "1.0")

    return "1.0"


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


@localization_app.route("/localization/version")
def get_translation_version():
    version = get_translation_version_from_file()
    return jsonify({"version": version})
