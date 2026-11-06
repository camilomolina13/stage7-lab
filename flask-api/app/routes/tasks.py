from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from ..extensions import db
from ..helpers import MAX_INT, get_json_body, get_or_404
from ..models import Task
from ..schemas import task_schema
from ..serializers import task_to_dict

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

NOT_FOUND = "Task not found."


@bp.get("")
def list_tasks():
    stmt = db.select(Task).order_by(Task.id)

    raw_project_id = request.args.get("project_id")
    if raw_project_id is not None:
        try:
            project_id = int(raw_project_id)
        except ValueError:
            raise ValidationError({"project_id": ["Not a valid integer."]})
        if project_id < 1 or project_id > MAX_INT:
            return jsonify([]), 200          # no puede existir ese proyecto
        stmt = stmt.where(Task.project_id == project_id)

    tasks = db.session.scalars(stmt).all()
    return jsonify([task_to_dict(t) for t in tasks]), 200


@bp.post("")
def create_task():
    data = task_schema.load(get_json_body())
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_to_dict(task)), 201


@bp.get("/<int:task_id>")
def get_task(task_id):
    task = get_or_404(Task, task_id, NOT_FOUND)
    return jsonify(task_to_dict(task)), 200


@bp.put("/<int:task_id>")
def update_task(task_id):
    task = get_or_404(Task, task_id, NOT_FOUND)
    data = task_schema.load(get_json_body())
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return jsonify(task_to_dict(task)), 200


@bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = get_or_404(Task, task_id, NOT_FOUND)
    db.session.delete(task)
    db.session.commit()
    return "", 204