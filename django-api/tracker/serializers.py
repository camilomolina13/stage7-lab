from rest_framework import serializers

from .helpers import MAX_INT
from .models import Project

STATUSES = ["TODO", "IN_PROGRESS", "DONE"]
PRIORITIES = ["LOW", "MEDIUM", "HIGH"]


class StrictCharField(serializers.CharField):
    """DRF acepta números como texto (123 -> "123"). Aquí solo se aceptan strings."""

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail("invalid")
        return super().to_internal_value(data)


class StrictIntegerField(serializers.IntegerField):
    """DRF acepta "1" y 1.0. Aquí solo se aceptan enteros reales."""

    default_error_messages = {"invalid": "Not a valid integer."}

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, int):
            self.fail("invalid")
        return data


class StrictChoiceField(StrictCharField):
    """Texto que debe estar en una lista de valores permitidos."""

    def __init__(self, choices, message, **kwargs):
        self.allowed = choices
        kwargs["error_messages"] = {"blank": message, "invalid_choice": message}
        super().__init__(trim_whitespace=False, **kwargs)

    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if value not in self.allowed:
            self.fail("invalid_choice")
        return value


class ProjectSerializer(serializers.Serializer):
    name = StrictCharField(max_length=150, trim_whitespace=True)
    description = StrictCharField(required=False, default="", allow_blank=True, trim_whitespace=False)


class TaskSerializer(serializers.Serializer):
    project_id = StrictIntegerField()
    title = StrictCharField(max_length=200, trim_whitespace=True)
    description = StrictCharField(required=False, default="", allow_blank=True, trim_whitespace=False)
    status = StrictChoiceField(
        STATUSES, "Must be one of: TODO, IN_PROGRESS, DONE.", required=False, default="TODO"
    )
    priority = StrictChoiceField(
        PRIORITIES, "Must be one of: LOW, MEDIUM, HIGH.", required=False, default="MEDIUM"
    )
    due_date = serializers.DateField(
        required=False,
        default=None,
        allow_null=True,
        error_messages={"invalid": "Not a valid date. Use YYYY-MM-DD."},
    )

    def validate_project_id(self, value):
        # Se ejecuta junto con las demás validaciones, así el error aparece
        # en el mismo 400 que los demás. Solo corre si project_id ya es un entero.
        if value < 1 or value > MAX_INT or not Project.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Project does not exist.")
        return value
