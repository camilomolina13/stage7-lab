import json

from rest_framework.exceptions import ValidationError
from rest_framework.negotiation import DefaultContentNegotiation

from .errors import ResourceNotFound

MAX_INT = 2_147_483_647   # máximo de un INTEGER en PostgreSQL


def get_or_404(model, pk, message):
    """Busca por id o lanza 404. Protege también de ids fuera del rango de INTEGER."""
    if pk < 1 or pk > MAX_INT:
        raise ResourceNotFound(message)
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise ResourceNotFound(message)


def get_json_body(request):
    """Devuelve el body como dict, o lanza el error '_schema' del contrato."""
    try:
        data = json.loads(request.body)
    except ValueError:                 # JSON roto o vacío
        data = None
    if not isinstance(data, dict):
        raise ValidationError({"_schema": ["Body must be a valid JSON object."]})
    return data


def save_changes(instance, data):
    """Guarda solo si algo cambió realmente (igual que SQLAlchemy en Flask)."""
    changed = [field for field, value in data.items() if getattr(instance, field) != value]
    if changed:
        instance.save(update_fields=changed)
        instance.refresh_from_db()     # trae el updated_at que puso el trigger
    return instance


class IgnoreClientContentNegotiation(DefaultContentNegotiation):
    """Siempre responde JSON, sin importar el header Accept (como hace Flask)."""

    def select_renderer(self, request, renderers, format_suffix=None):
        return (renderers[0], renderers[0].media_type)