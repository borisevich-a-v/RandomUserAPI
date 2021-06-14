"""Describe models for database"""
from . import db


class User(db.Model):
	"""Class user describes entity of user for database
	user_id:"""  # TODO

	__tablename__ = "users"
	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
	gender = db.Column(db.String)  # Maybe create another table?
	email = db.Column(db.String)
	phone = db.Column(db.String(32))
	cell = db.Column(db.String(32))
	nat = db.Column(db.String(8))  # Maybe create another table?
	# Name
	title = db.Column(db.String)  # Maybe create another table?
	first_name = db.Column(db.String)
	last_name = db.Column(db.String)
	# Location
	street_number = db.Column(db.Integer)
	street_name = db.Column(db.String)
	city = db.Column(db.String)  # Maybe create another table?
	state = db.Column(db.String)  # Maybe create another table?
	country = db.Column(db.String)  # Maybe create another table?
	postcode = db.Column(db.Integer)
	latitude = db.Column(db.String)
	longitude = db.Column(db.String)
	timezone_offset = db.Column(db.String)  # Maybe create another table?
	timezone_description = db.Column(db.String)  # Maybe create another table?
	# Login
	uuid = db.Column(db.String)
	username = db.Column(db.String)
	password = db.Column(db.String)
	salt = db.Column(db.String)
	md5 = db.Column(db.String(32))
	sha1 = db.Column(db.String(40))
	sha256 = db.Column(db.String(64))
	# Date of birth
	date_of_birth = db.Column(db.String(32))
	age = db.Column(db.SmallInteger)
	# registered
	registered_date = db.Column(db.String(32))
	registered_age = db.Column(db.SmallInteger)
	# id
	id_name = db.Column(db.String)
	id_value = db.Column(db.String)
	# Pictures
	picture_l = db.Column(db.String)
	picture_m = db.Column(db.String)
	picture_s = db.Column(db.String)


	def __repr__(self):
		args = [
			arg + "=" + "'" + str(self.__dict__[arg]) + "'"
			for arg in self.__dict__
			if not arg.startswith("_")
		]
		return "User(" + ", ".join(args) + ")"
