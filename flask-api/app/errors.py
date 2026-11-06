from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

from .extensions import db


class ResourceNotFound(Exception):
    """La lanzamos cuando un proyecto o tarea no existe (404)."""

    def __init__(self, message="Resource not found."):
        super().__init__(message)
        self.message = message


def error_response(code, message, status, details=None):
    body = {"error": {"code": code, "message": message}}
    if details is not None:          # 'details' solo existe en validation_error
        body["error"]["details"] = details
    return jsonify(body), status


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation(err):
        return error_response("validation_error", "Invalid input data.", 400, err.messages)

    @app.errorhandler(ResourceNotFound)
    def handle_not_found(err):
        return error_response("not_found", err.message, 404)

    @app.errorhandler(HTTPException)
    def handle_http(err):
        # Rutas que no existen (404) y métodos no permitidos (405)
        if err.code == 404:
            return error_response("not_found", "Resource not found.", 404)
        if err.code == 405:
            return error_response("method_not_allowed", "Method not allowed.", 405)
        return error_response("http_error", err.description, err.code)

    @app.errorhandler(SQLAlchemyError)
    def handle_database(err):
        db.session.rollback()        # deshace la transacción fallida
        app.logger.exception(err)
        return error_response("database_error", "Database error.", 500)

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        db.session.rollback()
        app.logger.exception(err)
        return error_response("server_error", "Unexpected server error.", 500)