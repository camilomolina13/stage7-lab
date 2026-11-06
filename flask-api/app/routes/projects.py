from flask import Blueprint, jsonify

from ..extensions import db
from ..helpers import get_json_body, get_or_404
from ..models import Project
from ..schemas import project_schema
from ..serializers import project_to_dict

bp = Blueprint("projects", __name__, url_prefix="/api/projects")

NOT_FOUND = "Project not found."

@bp.get("")
def list_projects():
    projects = db.session.scalars(db.select(Project).order_by(Project.id)).all()
    return jsonify([project_to_dict(p) for p in projects]), 200

@bp.post("")
def create_project():
    data = project_schema.load(get_json_body())   # lanza ValidationError si hay errores
    project = Project(**data)
    db.session.add(project)
    db.session.commit()
    return jsonify(project_to_dict(project)), 201

@bp.get("/<int:project_id>")
def get_project(project_id):
    project = get_or_404(Project, project_id, NOT_FOUND)
    return jsonify(project_to_dict(project)), 200

@bp.put("/<int:project_id>")
def update_project(project_id):
    project = get_or_404(Project, project_id, NOT_FOUND)   # 404 primero, luego el body
    data = project_schema.load(get_json_body())
    for key, value in data.items():
        setattr(project, key, value)
    db.session.commit()
    return jsonify(project_to_dict(project)), 200

@bp.delete("/<int:project_id>")
def delete_project(project_id):
    project = get_or_404(Project, project_id, NOT_FOUND)
    db.session.delete(project)    # las tareas se borran por el ON DELETE CASCADE
    db.session.commit()
    return "", 204