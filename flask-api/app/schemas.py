from marshmallow import EXCLUDE, Schema, ValidationError, fields, pre_load, validate, validates

from .extensions import db
from .models import Project

STATUSES = ["TODO", "IN_PROGRESS", "DONE"]
PRIORITIES = ["LOW", "MEDIUM", "HIGH"]
MAX_INT = 2_147_483_647  # máximo de un INTEGER en PostgreSQL

# Mensajes comunes del contrato
REQUIRED = "This field is required."
NULL = "This field may not be null."
NOT_STRING = "Not a valid string."


def text_messages():
    return {"required": REQUIRED, "null": NULL, "invalid": NOT_STRING}


def not_blank(value):
    if not value.strip():
        raise ValidationError("This field may not be blank.")


def strip_field(data, field_name):
    """Recorta espacios de un campo de texto (sin modificar el dict original)."""
    data = dict(data)
    if isinstance(data.get(field_name), str):
        data[field_name] = data[field_name].strip()
    return data


class ProjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE   # ignora id, created_at y cualquier campo desconocido

    name = fields.Str(
        required=True,
        error_messages=text_messages(),
        validate=[
            not_blank,
            validate.Length(max=150, error="Ensure this field has no more than 150 characters."),
        ],
    )
    description = fields.Str(load_default="", error_messages=text_messages())

    @pre_load
    def strip_name(self, data, **kwargs):
        return strip_field(data, "name")


class TaskSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    project_id = fields.Int(
        required=True,
        strict=True,   # rechaza "1" y 1.5: solo enteros reales
        error_messages={"required": REQUIRED, "null": NULL, "invalid": "Not a valid integer."},
    )
    title = fields.Str(
        required=True,
        error_messages=text_messages(),
        validate=[
            not_blank,
            validate.Length(max=200, error="Ensure this field has no more than 200 characters."),
        ],
    )
    description = fields.Str(load_default="", error_messages=text_messages())
    status = fields.Str(
        load_default="TODO",
        error_messages=text_messages(),
        validate=validate.OneOf(STATUSES, error="Must be one of: TODO, IN_PROGRESS, DONE."),
    )
    priority = fields.Str(
        load_default="MEDIUM",
        error_messages=text_messages(),
        validate=validate.OneOf(PRIORITIES, error="Must be one of: LOW, MEDIUM, HIGH."),
    )
    due_date = fields.Date(
        allow_none=True,
        load_default=None,
        error_messages={"invalid": "Not a valid date. Use YYYY-MM-DD."},
    )

    @pre_load
    def strip_title(self, data, **kwargs):
        return strip_field(data, "title")

    @validates("project_id")
    def project_must_exist(self, value, **kwargs):
        # Se ejecuta junto con las demás validaciones, así el error de
        # project_id aparece en el mismo 400 que los demás errores.
        if value < 1 or value > MAX_INT or db.session.get(Project, value) is None:
            raise ValidationError("Project does not exist.")

project_schema = ProjectSchema()
task_schema = TaskSchema()