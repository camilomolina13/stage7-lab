from flask import Flask
from flask_cors import CORS
from .config import Config
from .errors import register_error_handlers
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.sort_keys = False         # respeta el orden de campos del contrato
    app.url_map.strict_slashes = False

    CORS(app)
    db.init_app(app)

    from .routes.projects import bp as projects_bp
    from .routes.tasks import bp as tasks_bp
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)

    register_error_handlers(app)
    return app