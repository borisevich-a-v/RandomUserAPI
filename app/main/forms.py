"""Describe forms for pages"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, RadioField, StringField
from wtforms.validators import NumberRange, InputRequired, DataRequired, Length

from app.models import User


class NumberUsersToLoadForm(FlaskForm):
	"""Form for '/' page. Get number of users.
	This number of users will load to database"""

	__warn_msg = "You must enter number from 1 to 5000"
	number_load_users = IntegerField(
		"How many users load from API?",
		validators=[NumberRange(min=1, max=5000, message=__warn_msg)],
	)
	submit_load_users = SubmitField("Load users")


class UsersPerPageForm(FlaskForm):
	__warn_msg = "Must be integer, more than 1"
	number_pagination = IntegerField(
		"How many users to show on the page?",
		validators=[NumberRange(min=1, max=10000, message=__warn_msg)],
	)
	submit_pagination = SubmitField("Ok")


class ChangeUserDataForm(FlaskForm):

	gender = RadioField("Gender", choices=['male', 'female'])
	email = StringField('Email')
	phone = StringField('Phone', validators=[Length(0, 32)])
	cell = StringField('Cell', validators=[Length(0, 32)])
	nat = StringField('Nat', validators=[Length(0, 8)])
	# Name
	title = StringField('Title')
	first_name = StringField('First name')
	last_name = StringField('Last name')
	# Location
	street_number = IntegerField('Street number')
	street_name = StringField('Street name')
	city = StringField('City')
	state = StringField('State')
	country = StringField('Country')
	postcode = StringField('Postcode')
	latitude = StringField('Latitude')
	longitude = StringField('Longitude')
	timezone_offset = StringField('Timezone offset')
	timezone_description = StringField('Timezone description')
	# Login
	uuid = StringField('uuid')
	username = StringField('Username')
	password = StringField('Password')
	salt = StringField('Salt')
	md5 = StringField('md5', validators=[Length(0, 32)])
	sha1 = StringField('sha1', validators=[Length(0, 40)])
	sha256 = StringField('sha256', validators=[Length(0, 64)])
	# Date of birth
	date_of_birth = StringField('date_of_birth', validators=[Length(0, 32)])
	age = IntegerField("age", validators=[NumberRange(min=0, max=1000)])
	# registered
	registered_date = StringField('registered_date', validators=[Length(0, 32)])
	registered_age = IntegerField("registered_age", validators=[NumberRange(min=0, max=1000)])
	# id
	id_name = StringField('id_name')
	id_value = StringField('id_value')
	# Pictures
	picture_l = StringField('picture_l')
	picture_m = StringField('picture_m')
	picture_s = StringField('picture_s')



	submit_change = SubmitField('Change')

