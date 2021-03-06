"""Contain the function create_app() that init an app"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    """init an app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from app.main.views import main as main_blueprints

    app.register_blueprint(main_blueprints)
    return app
