import logging

from django.db import DatabaseError
from django.http import Http404, JsonResponse
from rest_framework.exceptions import MethodNotAllowed, NotFound, ValidationError
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class ResourceNotFound(Exception):
    """La lanzamos cuando un proyecto o tarea no existe (404)."""

    def __init__(self, message="Resource not found."):
        super().__init__(message)
        self.message = message


def error_body(code, message, details=None):
    body = {"error": {"code": code, "message": message}}
    if details is not None:             # 'details' solo existe en validation_error
        body["error"]["details"] = details
    return body


def plain(detail):
    """Convierte los errores de DRF (ErrorDetail) a dict/list/str normales."""
    if isinstance(detail, dict):
        return {key: plain(value) for key, value in detail.items()}
    if isinstance(detail, list):
        return [plain(item) for item in detail]
    return str(detail)


def custom_exception_handler(exc, context):
    """DRF llama a esta función con CUALQUIER excepción de una vista."""
    if isinstance(exc, ValidationError):
        details = plain(exc.detail)
        if isinstance(details, list):                    # error sin campo
            details = {"_schema": details}
        return Response(error_body("validation_error", "Invalid input data.", details), status=400)

    if isinstance(exc, ResourceNotFound):
        return Response(error_body("not_found", exc.message), status=404)

    if isinstance(exc, (NotFound, Http404)):
        return Response(error_body("not_found", "Resource not found."), status=404)

    if isinstance(exc, MethodNotAllowed):
        return Response(error_body("method_not_allowed", "Method not allowed."), status=405)

    if isinstance(exc, DatabaseError):                   # incluye IntegrityError y OperationalError
        logger.error("Database error", exc_info=exc)
        return Response(error_body("database_error", "Database error."), status=500)

    logger.error("Unexpected error", exc_info=exc)
    return Response(error_body("server_error", "Unexpected server error."), status=500)


def unknown_route(request, *args, **kwargs):
    """404 en JSON para rutas que no existen (ej: /api/nada o /api/projects/abc)."""
    return JsonResponse(error_body("not_found", "Resource not found."), status=404)