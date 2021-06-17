"""routine at server start"""
import os

from app import db
from app.api_data import collect_more_users
from app.models import User


def create_paths():
    """Create directories for images"""
    dirpaths = ["app/static/portraits/large/1", "app/static/portraits/thumbnail/1"]
    for path in dirpaths:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))


def make_routines():
    """Tasks for starting server"""
    create_paths()

    from epam import app

    with app.app_context():
        db.create_all()  # Не могу нормально создать таблицу. Как правильно?
        if User.query.count() < 1000:
            collect_more_users(1000 - User.query.count())
