from flask import Blueprint, current_app
import werkzeug
import werkzeug.exceptions

handler_blueprint: Blueprint = Blueprint('handler_blueprint', __name__)


@handler_blueprint.app_errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    current_app.logger.error(f"User submitted bad request, error: {e}")
    return {"error": "bad request!", "status": 400}


@handler_blueprint.app_errorhandler(werkzeug.exceptions.BadRequestKeyError)
def handle_key_request_error(e):
    current_app.logger.error(f"User request with Key Error, error: {e}")
    return {"error": 'key error!', "status": 400}


@handler_blueprint.app_errorhandler(werkzeug.exceptions.NotFound)
def handle_not_found(e):
    current_app.logger.error(
        f"User requested resource that does not exist: {e}")
    return {"error": 'Resource not found!', "status": 404}


@handler_blueprint.app_errorhandler(werkzeug.exceptions.UnsupportedMediaType)
def handle_unsupported_media(e):
    current_app.logger.error(
        f"User sent request with unsupported media type: {e}")
    return {"error": 'Something was wrong with the formatting of your request!', "status": 412}


@handler_blueprint.app_errorhandler(KeyError)
def handle_key_error(e):
    current_app.logger.error(f"User request with Key Error, error: {e}")
    return {"error": 'key error!', "status": 400}
