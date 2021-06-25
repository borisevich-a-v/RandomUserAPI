"""Configurations for app"""
import os
from abc import ABCMeta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(metaclass=ABCMeta):
    """Base class configuration"""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "password"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIN_PAGE_ROW_PER_PAGE = 50
    ALLOWED_EXTENSIONS = {"jpg"}
    MAX_CONTENT_LENGTH = 1024 * 1024

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Config for development purposes"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    """Config for testing purpose"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Config):
    """Config for production"""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
