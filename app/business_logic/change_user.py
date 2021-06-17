"""This module contains functions for work with users data"""
import os
import tempfile
from pathlib import Path
from random import randint
from typing import Generator, Type

from flask import current_app, render_template
from flask_wtf import FlaskForm
from PIL import Image
from werkzeug.utils import secure_filename

from app.app import db
from app.main.forms import ChangeUserDataForm
from app.models import User


def allowed_file(filename):
    """Check that file allowed"""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


def get_user_template(user_id):
    """Render user_template by user_id
    :param user_id: user_id in database
    :type user_id: `int`"""
    user = User.query.filter_by(user_id=user_id).first_or_404(user_id)
    return render_template("user.html", user=user, user_id=user_id)


def resize_image(path):
    """Resize image and save it in file system and return their paths"""
    file_ids = [
        int(os.path.splitext(filename)[0])
        for filename in (os.listdir("app/static/portraits/large") or ["0.jpg"])
    ]
    file_id = str(max(file_ids) + 1)

    with Image.open(path) as img:
        img.thumbnail((128, 128))
        path_large = Path("app/static/portraits/large", file_id + ".jpg")
        img.save(path_large)

        img.thumbnail((48, 48))
        path_thumbnail = Path("app/static/portraits/thumbnail", file_id + ".jpg")
        img.save(path_thumbnail)
    return file_id + ".jpg"


def get_portraits(file, filename):
    """Save portraits in file system and return their paths"""
    with tempfile.TemporaryDirectory() as tmpdirname:
        filename = filename + str(randint(1, 10 ** 9))
        path = Path(tmpdirname, filename)
        file.save(path)
        return resize_image(path)


def remove_pictures(*paths):
    """Remove pictures by paths"""
    for path in paths:
        try:
            os.remove(path)
        except (FileNotFoundError, IsADirectoryError):
            pass


def get_form_fields(form: Type[FlaskForm]) -> Generator:
    """Retern generator. Generator yield form field's data attributes"""
    return (
        attribute
        for attribute in form.__dict__
        if not (
            attribute.startswith("_")
            or attribute.startswith("<")
            or attribute.startswith("submit")
        )
    )


def change_data(user_id, form):
    """Change user by user_id. Get data from a form"""
    user = User.query.filter(User.user_id == user_id).first()
    for attribute in get_form_fields(ChangeUserDataForm):
        setattr(user, attribute, form[attribute].data)
    db.session.commit()


def change_portrait(user_id, file):
    """Change user's portrait. file is been a new portrait"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        portrait_name = get_portraits(file, filename)
        user = User.query.filter(User.user_id == user_id).first()
        remove_pictures(
            Path("app" + user.portrait_large), Path("app" + user.portrait_thumbnail)
        )
        src = "/static/portraits/"
        user.portrait_large = src + "large/" + portrait_name
        user.portrait_thumbnail = src + "thumbnail/" + portrait_name
        db.session.commit()
        return "Success"
    return False


def create_user(form):
    """Add new user row"""
    user = User()
    for attribute in get_form_fields(ChangeUserDataForm):
        setattr(user, attribute, form[attribute].data)
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    return user.user_id
