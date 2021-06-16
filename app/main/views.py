"""In this module describes all routes"""
import os
from random import randint

from PIL import Image
from flask import current_app, render_template, request, flash, url_for
from sqlalchemy import func, cast, Integer
from werkzeug.utils import redirect, secure_filename

from .. import db
from ..api.api_data import get_more_users
from ..models import User
from . import main
from .forms import NumberUsersToLoadForm, UsersPerPageForm, ChangeUserDataForm


@main.route("/", methods=["GET", "POST"])
def index():
    """Main page"""
    load_user_form = NumberUsersToLoadForm()
    row_on_page_form = UsersPerPageForm()

    if "submit_load_users" in request.form and load_user_form.validate_on_submit():
        get_more_users(load_user_form.number_load_users.data)
        load_user_form.number_load_users.data = 0

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


def get_user_template(user_id):
    """Render user_template by user_id"""
    user = User.query.filter_by(user_id=user_id).first_or_404(user_id)
    return render_template("user.html", user=user, user_id=user_id)


@main.route("/user/<user_id>")
def user(user_id):
    """Return user profile by id"""
    user_id = int(user_id)
    return get_user_template(user_id)


@main.route("/random")
def user_random():
    """Return user profile by id"""
    number_of_users = User.query.count()
    user_id = randint(1, number_of_users)
    return get_user_template(user_id)


@main.route("/user/<user_id>/change_data", methods=["GET", "POST"])
def change_user_data(user_id):
    """User change form"""
    change_form = ChangeUserDataForm()
    user = User.query.filter(User.user_id == user_id).first()

    attributes = (
        attribute
        for attribute in ChangeUserDataForm.__dict__
        if not (
            attribute.startswith("_")
            or attribute.startswith("<")
            or attribute.startswith("submit")
    )
    )
    if change_form.validate_on_submit():
        for attribute in attributes:
            setattr(user, attribute, change_form[attribute].data)
        db.session.commit()
        return redirect(f"/user/{user_id}")

    for attribute in attributes:
        change_form[attribute].data = getattr(user, attribute)
    return render_template("change_user_data.html", user_id=user_id, form=change_form)


def allowed_file(filename):
    """Проверка, что файл разрешён"""
    return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            in current_app.config["ALLOWED_EXTENSIONS"]
    )


def resize_and_save_images(path):
    file_id = db.session.query(func.max(cast(User.portrait_id, Integer))).one()[
        0]  # TODO
    file_id += 1
    file_id = str(max(file_id, 2000))
    with Image.open(path) as im:
        im.thumbnail((128, 128))
        im.save('app/static/portraits/large/' + file_id + '.jpg')
        im.thumbnail((72, 72))
        im.save('app/static/portraits/medium/' + file_id + '.jpg')
        im.thumbnail((48, 48))
        im.save('app/static/portraits/thumbnail/' + file_id + '.jpg')
    return file_id


@main.route("/user/<user_id>/change_portrait", methods=["GET", "POST"])
def change_user_portrait(user_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            file_id = resize_and_save_images(path)
            user = User.query.filter(User.user_id == user_id).first()
            user.portrait_id = int(file_id)
            db.session.commit()
        return redirect(f"/user/{user_id}")

    return render_template("change_user_portrait.html")
