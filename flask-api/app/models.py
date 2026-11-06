from .extensions import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # server_default: Flask no envía este valor, lo pone PostgreSQL (DEFAULT NOW())
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    # El trigger de PostgreSQL actualiza este campo en cada UPDATE
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)