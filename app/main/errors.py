"""Error handlers"""
from flask import render_template

from app.main import main


@main.app_errorhandler(404)
def page_not_found(error):
    """Handle 404 error"""
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def internal_server_error(error):
    """Handle 500 error"""
    return render_template("500.html"), 500
