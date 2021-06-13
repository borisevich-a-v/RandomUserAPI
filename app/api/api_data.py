"""Contain functions to communicate with API and convert raw data"""
import json
from typing import List

import requests

from app import db
from app.models import User

API_URL = "https://randomuser.me/api"


class APIError(Exception):
    """General API error"""

    ...


class BadAPIStatusCode(APIError):
    """Raised when API status code is not 200"""

    ...


class BadRawJSON(APIError):
    """Return wrong number of people"""

    ...


def make_request(user_number: int) -> str:
    """Make request to the API and return response.text"""
    response = requests.get(API_URL, params={"results": user_number})
    if response.status_code != 200:
        raise BadAPIStatusCode(f"{API_URL} return {response.status_code}")
    return response.text


def convert_raw_json(raw_json: str, user_numbers: int) -> dict:
    """Convert raw JSON to a list of a users"""
    try:
        data = json.loads(raw_json)
        if int(data["info"]["results"]) != user_numbers:
            raise BadRawJSON
    except (ValueError, KeyError) as error:
        raise BadRawJSON from error

    return data["results"]


def convert_into_users(jsons_dict: dict) -> List[User]:
    """Convert specific JSON into User"""
    users = []
    for json_user in jsons_dict:
        user = User(
            sex=json_user["gender"],
            first_name=json_user["name"]["first"],
            last_name=json_user["name"]["last"],
            phone=json_user["phone"],
            email=json_user["email"],
            location=json_user["location"]["city"],
            photo="photo",
        )
        users.append(user)
    return users


def get_more_users(number: int) -> List[User]:
    """Return list of dicts. Each dict contains info about users"""
    users = convert_into_users(convert_raw_json(make_request(number), number))
    print(users[0])
    db.create_all()
    db.session.add_all(users)
    db.session.commit()
    return users
