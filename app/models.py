"""Describe models for database"""
from typing import List

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

    @classmethod
    def _convert_from_json(cls, user_json: dict):  # TODO -> return
        """Convert user's data from JSON to `class` USER
        :param user_json: user's data in JSON
        :type user_json: :class:`dict`
        :return: users data in :class:`User` format
        :rtype: :class:`User`"""
        return cls(
            gender=user_json["gender"],
            email=user_json["email"],
            phone=user_json["phone"],
            first_name=user_json["name"]["first"],
            last_name=user_json["name"]["last"],
            street_name=user_json["location"]["street"]["name"],
            city=user_json["location"]["city"],
            state=user_json["location"]["state"],
            country=user_json["location"]["country"],
            postcode=user_json["location"]["postcode"],
            portrait_large=user_json["picture"]["large"],
            portrait_thumbnail=user_json["picture"]["thumbnail"],
        )

    @classmethod
    def convert_into_users(cls, users_array: List[dict]):  # TODO -> List[User]:
        """Convert specific JSON into User
        :param users_array: list of JSON's
        :type users_array: `list`
        :return: list of :class:`User`
        :rtype: `list`"""
        return [cls._convert_from_json(user_data) for user_data in users_array]
