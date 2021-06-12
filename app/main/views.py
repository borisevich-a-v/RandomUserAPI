from random import randint

from flask import render_template

from . import main
from .forms import UserNumberForm
from ..models import get_users


@main.route("/", methods=["GET", "POST"])
def index():
	"""Main page"""
	number = None
	form = UserNumberForm()
	users = get_users(2)
	if form.validate_on_submit():
		number = form.number.data
		form.number.data = ""
	return render_template("index.html", form=form, number=number, users=users)


def get_user_template(user_id):
	"""Render user_template by user_id"""
	return render_template("user.html", user_id=user_id)


@main.route("/user/<user_id>")
def user(user_id):
	"""Return user profile by id"""
	try:
		user_id = int(user_id)
	except TypeError:
		return render_template('404.html')
	return get_user_template(user_id)


@main.route("/random")
def user_random():
	"""Return user profile by id"""
	number_of_users = 1000
	user_id = randint(1, number_of_users)
	return get_user_template(user_id)
