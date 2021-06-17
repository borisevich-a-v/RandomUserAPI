"""In this module describes all routes"""
from random import randint

from flask import current_app, flash, render_template, request, url_for
from werkzeug.utils import redirect

from app.business_logic.api_data import collect_more_users_thread
from app.business_logic.change_user import (
    change_data,
    change_portrait,
    create_user,
    get_form_fields,
    get_user_template,
)
from app.main import main
from app.main.forms import ChangeUserDataForm, NumberUsersToLoadForm, UsersPerPageForm
from app.models import User


@main.route("/", methods=["GET", "POST"])
def index():
    """Main page"""
    load_user_form = NumberUsersToLoadForm()
    row_on_page_form = UsersPerPageForm()

    if "submit_load_users" in request.form and load_user_form.validate_on_submit():
        collect_more_users_thread(load_user_form.number_load_users.data)
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

    if change_form.validate_on_submit():
        change_data(user_id, change_form)
        return redirect(f"/{user_id}")

    for attribute in get_form_fields(ChangeUserDataForm):
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
        if not change_portrait(user_id, file) == "Success":
            flash("Bad file. Only jpg allowed.")
            return redirect(request.url)
        return redirect(f"/{user_id}")
    return render_template("change_user_portrait.html")


@main.route("/new_user", methods=["GET", "POST"])
def new_user_data():
    """Create new user"""
    form = ChangeUserDataForm()
    if form.validate_on_submit():
        user_id = create_user(form)
        return redirect(f"/{user_id}/change_portrait")
    return render_template("change_user_data.html", form=form, header="Create New User")
