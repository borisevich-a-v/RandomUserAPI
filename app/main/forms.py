"""Forms for pages"""

from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, StringField, SubmitField
from wtforms.validators import Length, NumberRange


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


class ChangeUserDataForm(FlaskForm):
    """Form. Serve to get new user's data"""

    gender = RadioField("Gender", choices=["male", "female"])
    email = StringField("Email")
    phone = StringField("Phone", validators=[Length(0, 32)])

    first_name = StringField("First name")
    last_name = StringField("Last name")

    street_name = StringField("Street name")
    city = StringField("City")
    state = StringField("State")
    country = StringField("Country")
    postcode = StringField("Postcode")

    submit_change = SubmitField("Ok")
