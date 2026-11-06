from datetime import timezone

def to_utc_iso(value):
    """Convierte un datetime a '2026-11-06T14:30:00Z'."""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def project_to_dict(project):
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": to_utc_iso(project.created_at),
    }

def task_to_dict(task):
    return {
        "id": task.id,
        "project_id": task.project_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "created_at": to_utc_iso(task.created_at),
        "updated_at": to_utc_iso(task.updated_at),
    }