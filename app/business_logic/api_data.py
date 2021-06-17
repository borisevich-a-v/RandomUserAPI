"""Contain functions to communicate with API and convert raw data"""
import json
from threading import Thread
from typing import List

import requests

from app import db
from app.models import User

API_URL = "https://randomuser.me/api"


class APIError(Exception):
    """General API error"""

    ...


class BadAPIResponse(APIError):
    """API's response is bad"""

    ...


class BadRawJSON(APIError):
    """JSON has some problems"""

    ...


def get_users_json(user_number: int) -> List[dict]:
    """Convert raw JSON to a list of a users
    :param user_number: number of users to load from API
    :type user_number: :class:`int`
    :return: List of JSONs with users
    :rtype: :class:`list`"""
    response = requests.get(API_URL, params={"results": user_number})
    if not response.ok:
        raise BadAPIResponse(f"{API_URL} status code {response.status_code}")
    try:
        data = json.loads(response.text)
        if int(data["info"]["results"]) != user_number:
            raise BadRawJSON
    except (ValueError, KeyError) as error:
        raise BadRawJSON from error
    print(data["results"])
    return data["results"]


def convert_user(user_data: dict) -> User:
    """Convert user's data from JSON to `class` USER
    :param user_data: user's data in JSON
    :type user_data: :class:`dict`
    :return: users data in :class:`User` format
    :rtype: :class:`User`"""
    return User(
        gender=user_data["gender"],
        email=user_data["email"],
        phone=user_data["phone"],
        first_name=user_data["name"]["first"],
        last_name=user_data["name"]["last"],
        street_name=user_data["location"]["street"]["name"],
        city=user_data["location"]["city"],
        state=user_data["location"]["state"],
        country=user_data["location"]["country"],
        postcode=user_data["location"]["postcode"],
        portrait_large=user_data["picture"]["large"],
        portrait_thumbnail=user_data["picture"]["thumbnail"],
    )


def convert_into_users(users_array: List[dict]) -> List[User]:
    """Convert specific JSON into User
    :param users_array: list of JSON's
    :type users_array: `list`
    :return: list of :class:`User`
    :rtype: `list`"""
    return [convert_user(user_data) for user_data in users_array]


def collect_more_users(number: int) -> None:
    """Add more users into database from API
    :param number: number of users to add
    :type number: `int`"""
    users = convert_into_users(get_users_json(number))
    from random_user_api import app

    with app.app_context():
        db.session.add_all(users)
        db.session.commit()


def collect_more_users_thread(number: int) -> None:
    """Create thread and run in it collect_more_users
    :param number: number of users to add
    :type number: `int`"""
    get_users_task = Thread(
        target=collect_more_users,
        args=(number,),
        daemon=True,
    )
    get_users_task.start()
