"""Describe models for database"""
from app.app import db


class User(db.Model):
    """Class user describes entity of user for database"""

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    gender = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String(32))

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    street_name = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    postcode = db.Column(db.Integer)

    portrait_large = db.Column(db.String, default="")
    portrait_thumbnail = db.Column(db.String, default="")

    def __repr__(self):
        args = [
            arg + "=" + "'" + str(self.__dict__[arg]) + "'"
            for arg in self.__dict__
            if not arg.startswith("_")
        ]
        return "User(" + ", ".join(args) + ")"
