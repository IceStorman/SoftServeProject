from flask_smorest import Blueprint
from dto.api_output import CountriesOutput
from service.api_logic.countries_logic import get_countries
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response
from logger.logger import Logger


logger = Logger("logger", "all.log")

countries_app = Blueprint('countries_app', __name__, description="Country information", url_prefix='/countries')


@countries_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@countries_app.route('/', methods=['GET'])
@logger.log_function_call()
@countries_app.response(200, CountriesOutput(many=True))
def get_countries_endpoint():
    """Get all countries information"""
    try:
        countries = get_countries()
        return countries

    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        return get_custom_error_response(e)