from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange


class UserNumberForm(FlaskForm):
	warn_msg = "You must enter number from 1 to 5000"
	number = IntegerField(
		"How many users load from API?",
		validators=[NumberRange(min=1, max=5000, message=warn_msg)],
	)
	submit = SubmitField("Load users")
