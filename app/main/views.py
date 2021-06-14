"""In this module describes all routes"""
from random import randint

from flask import current_app, render_template, request, url_for
from werkzeug.utils import redirect

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


@main.route("/user/<user_id>/change", methods=["GET", "POST"])
def change_user(user_id):
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
		return redirect(f'/user/{user_id}')

	for attribute in attributes:
		change_form[attribute].data = getattr(user, attribute)
	return render_template(
		"change_user_data.html", user_id=user_id, form=change_form
	)
