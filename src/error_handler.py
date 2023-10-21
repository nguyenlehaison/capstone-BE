from needed_services import server_response
from auth.auth import AuthError


def unprocessable(error):
    return server_response(
        success=None,
        message="unprocessable",
        code=422
    )


def bad_request(error):
    return server_response(
        success=None,
        message="bad request",
        code=400
    )


def not_found(error):
    return server_response(
        success=False,
        message="resource not found",
        code=404
    )


def server_error(error):
    return server_response(
        success=False,
        message="server error",
        code=500
    )


def auth_error(error):
    return server_response(
        success=False,
        message=error.error['description'],
        code=error.status_code
    )


def create_error_handler(app):
    app.register_error_handler(422, unprocessable)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, not_found)
    app.register_error_handler(422, server_error)
    app.register_error_handler(AuthError, auth_error)
