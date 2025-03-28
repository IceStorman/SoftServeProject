from dependency_injector.wiring import inject, Provide
from api.container.container import Container
from flask import Blueprint, request
from exept.handle_exeptions import handle_exceptions, get_custom_error_response
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from logger.logger import Logger
from service.api_logic.comments_logic import CommentsService
from dto.api_input import InputCommentDTO
from dto.common_response import CommonResponse

logger = Logger("logger", "all.log")

comments_app = Blueprint('comments_app', __name__)

@comments_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@comments_app.route('/save', methods=['POST'])
@logger.log_function_call()
@handle_exceptions
@inject
def save_comment(service: CommentsService = Provide[Container.comments_service]):
    try:
        data = request.get_json()
        dto = InputCommentDTO().load(data)
        service.save_comment(dto)

        return CommonResponse().to_dict()

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)


@comments_app.route('/edit', methods=['POST'])
@logger.log_function_call()
@handle_exceptions
@inject
def edit_comment(service: CommentsService = Provide[Container.comments_service]):
    try:
        data = request.get_json()
        dto = InputCommentDTO().load(data)
        service.edit_comment(dto)

        return CommonResponse().to_dict()

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)


@comments_app.route('/get', methods=['GET'])
@logger.log_function_call()
@handle_exceptions
@inject
def get_comments(service: CommentsService = Provide[Container.comments_service]):
    try:
        dto = InputCommentDTO().load(request.args.to_dict())
        comments = service.get_comments(dto)

        return comments

    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)


@comments_app.route('/delete', methods=['DELETE'])
@logger.log_function_call()
@handle_exceptions
@inject
def delete_comment(service: CommentsService = Provide[Container.comments_service]):
    try:
        data = request.get_json()
        dto = InputCommentDTO().load(data)
        service.delete_comment(dto)

        return CommonResponse().to_dict()

    except CustomQSportException as e:
        logger.error(f"Error in DELETE /: {str(e)}")
        get_custom_error_response(e)
