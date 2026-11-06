from flask import request
from marshmallow import ValidationError

from .errors import ResourceNotFound
from .extensions import db

MAX_INT = 2_147_483_647

def get_or_404(model, item_id, message):
    """Busca por id o lanza 404. Protege también de ids fuera del rango de INTEGER."""
    if item_id < 1 or item_id > MAX_INT:
        raise ResourceNotFound(message)
    item = db.session.get(model, item_id)
    if item is None:
        raise ResourceNotFound(message)
    return item

def get_json_body():
    """Devuelve el body como dict, o lanza el error '_schema' del contrato."""
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        raise ValidationError({"_schema": ["Body must be a valid JSON object."]})
    return data