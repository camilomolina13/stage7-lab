import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

# El .env está en la raíz del repo: flask-api/app/config.py -> parents[2]
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.getenv('DB_USER', 'tracker')}:"
        f"{quote_plus(os.getenv('DB_PASSWORD', 'tracker_pass'))}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5433')}/" #I have changed the port because 5432 is occupied by PostgreSQL.
        f"{os.getenv('DB_NAME', 'project_tracker')}" #disables the system for tracking object modifications in the database.
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False