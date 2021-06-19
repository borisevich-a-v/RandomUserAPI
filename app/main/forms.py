"""Forms for pages"""
import phonenumbers
from flask_wtf import FlaskForm
from phonenumbers import NumberParseException
from wtforms import IntegerField, RadioField, StringField, SubmitField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError


class NumberUsersToLoadForm(FlaskForm):
    """Form. Get number of users. This number of users
    will load to database with collect_more_users()"""

    __warn_msg = "You must enter number from 1 to 5000"
    number_load_users = IntegerField(
        "How many users load from API?",
        validators=[NumberRange(min=1, max=5000, message=__warn_msg)],
    )
    submit_load_users = SubmitField("Load users")


class UsersPerPageForm(FlaskForm):
    """Form. Get number of users. This number of users will
    show in table per page"""

    __warn_msg = "Must be integer, more than 1"
    number_pagination = IntegerField(
        "How many users to show on the page?",
        validators=[NumberRange(min=1, max=10000, message=__warn_msg)],
    )
    submit_pagination = SubmitField("Ok")


def check_phone(form, field):
    """Validator for phone field"""
    if len(field.data) > 16:
        raise ValidationError("Invalid phone number.")
    try:
        input_number = phonenumbers.parse(field.data)
        if len(str(input_number.national_number)) != 10:
            raise ValidationError("Invalid phone number.")
    except NumberParseException as error:
        raise ValidationError("Invalid phone number.") from error


class ChangeUserDataForm(FlaskForm):
    """Form. Serve to get new user's data"""

    gender = RadioField("Gender", choices=["male", "female", "other"])
    email = StringField("Email", validators=[Email(), DataRequired()])
    phone = TelField("Phone", validators=[check_phone, DataRequired()])

    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])

    street_name = StringField("Street name")
    city = StringField("City")
    state = StringField("State")
    country = StringField("Country")
    postcode = StringField("Postcode")

    submit_change = SubmitField("Ok")
