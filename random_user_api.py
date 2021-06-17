"""entry point"""
import os

from flask_migrate import Migrate

from app import create_app, db
from app.business_logic.start_server import make_routines

app = create_app(os.getenv("FLASK_CONFIG") or "development")
migrate = Migrate(app, db)
make_routines()
