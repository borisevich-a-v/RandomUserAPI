"""Describe models for database"""
from . import db


class User(db.Model):
    """Class user describes entity of user for database
    user_id:"""  # TODO

    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    sex = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String(16))
    email = db.Column(db.String)
    location = db.Column(db.String)
    photo = db.Column(db.String)

    def __repr__(self):
        args = [
            arg + "=" + "'" + self.__dict__[arg] + "'"
            for arg in self.__dict__
            if not arg.startswith("_")
        ]
        return "User(" + ", ".join(args) + ")"
