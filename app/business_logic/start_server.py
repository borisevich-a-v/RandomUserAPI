"""routine at server start"""
import os

from app.app import db
from app.business_logic.api_data import collect_more_users
from app.models import User


def create_paths():
    """Create directories for images"""
    dirpaths = ["app/static/portraits/large/1", "app/static/portraits/thumbnail/1"]
    for path in dirpaths:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))


def load_users_up_to_n(number):
    """Load users from API up to 1000"""
    from random_user_api import app

    with app.app_context():
        db.create_all()
        if User.query.count() < number:
            collect_more_users(number - User.query.count())


def make_routines():
    """Tasks for starting server"""
    create_paths()
    load_users_up_to_n(1000)
