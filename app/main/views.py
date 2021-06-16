"""In this module describes all routes"""
import os
import tempfile
from pathlib import Path
from random import randint
from threading import Thread
from typing import Generator

from flask import current_app, flash, render_template, request, url_for
from flask_wtf import FlaskForm
from PIL import Image
from werkzeug.utils import redirect, secure_filename

from .. import db
from ..api.api_data import collect_more_users
from ..models import User
from . import main
from .forms import ChangeUserDataForm, NumberUsersToLoadForm, UsersPerPageForm


@main.route("/", methods=["GET", "POST"])
def index():
    """Main page"""
    load_user_form = NumberUsersToLoadForm()
    row_on_page_form = UsersPerPageForm()

    if "submit_load_users" in request.form and load_user_form.validate_on_submit():
        get_users_task = Thread(
            target=collect_more_users,
            args=(load_user_form.number_load_users.data,),
            daemon=True,
        )
        get_users_task.start()
        load_user_form.number_load_users.data = 0
        flash(
            "Users downloading. The page needs to be refreshed when the downloading is complete."
        )
        return redirect(url_for("main.index"))

    if "submit_pagination" in request.form and row_on_page_form.validate_on_submit():
        current_app.config[
            "MAIN_PAGE_ROW_PER_PAGE"
        ] = row_on_page_form.number_pagination.data
        row_on_page_form.number_pagination.data = 0

    page = request.args.get("page", 1, type=int)
    pagination = User.query.paginate(
        page, per_page=current_app.config["MAIN_PAGE_ROW_PER_PAGE"], error_out=True
    )
    users = pagination.items
    return render_template(
        "index.html",
        users_to_load_form=load_user_form,
        users_per_page_form=row_on_page_form,
        users=users,
        pagination=pagination,
    )


@main.route("/<user_id>")
def user_profile(user_id):
    """Return user profile by id"""
    try:
        return get_user_template(user_id)
    except ValueError:
        return render_template("404.html"), 404


@main.route("/random")
def user_random():
    """Return user profile by id"""
    user_id = randint(1, User.query.count())
    return get_user_template(user_id)


@main.route("/<user_id>/change_data", methods=["GET", "POST"])
def change_user_data(user_id):
    """User change form"""
    change_form = ChangeUserDataForm()
    user = User.query.filter(User.user_id == user_id).first()

    attributes = generate_form_fields_names(ChangeUserDataForm)

    if change_form.validate_on_submit():
        for attribute in attributes:
            setattr(user, attribute, change_form[attribute].data)
        db.session.commit()
        return redirect(f"/{user_id}")

    for attribute in attributes:
        change_form[attribute].data = getattr(user, attribute)
    return render_template(
        "change_user_data.html",
        form=change_form,
        header=f"Change user profile: {user_id}",
    )


@main.route("/<user_id>/change_portrait", methods=["GET", "POST"])
def change_user_portrait(user_id):
    """For change or add user portrait"""
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
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
        return redirect(f"/{user_id}")
    return render_template("change_user_portrait.html")


@main.route("/new_user", methods=["GET", "POST"])
def new_user_data():
    """Create new user"""
    form = ChangeUserDataForm()
    attributes = generate_form_fields_names(ChangeUserDataForm)
    if form.validate_on_submit():
        user = User()
        for attribute in attributes:
            setattr(user, attribute, form[attribute].data)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return redirect(f"/{user.user_id}/change_portrait")
    return render_template("change_user_data.html", form=form, header="Create New User")


def generate_form_fields_names(form: FlaskForm) -> Generator:
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
