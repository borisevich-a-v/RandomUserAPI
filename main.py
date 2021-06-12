from flask import Flask, render_template
from random import randint

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "word"  # TODO


class UserNumberForm(FlaskForm):
	warn_msg = "You must enter number from 1 to 5000"
	number = IntegerField(
		"How many users load from API?",
		validators=[NumberRange(min=1, max=5000, message=warn_msg)],
	)
	submit = SubmitField('Load users')


@app.route("/", methods=['GET', 'POST'])
def index():
	"""Main page"""
	number = None
	form = UserNumberForm()
	if form.validate_on_submit():
		number = form.number.data
		form.number.data = ''
	return render_template("index.html", form=form, number=number)


def get_user_template(user_id):
	"""Render user_template by user_id"""
	return render_template("user.html", user_id=user_id)


@app.route("/<user_id>")
def user(user_id):
	"""Return user profile by id"""
	try:
		user_id = int(user_id)
	except TypeError:
		raise
	return get_user_template(user_id)


@app.route("/random")
def user_random():
	"""Return user profile by id"""
	number_of_users = 1000
	user_id = randint(1, number_of_users)
	return get_user_template(user_id)
