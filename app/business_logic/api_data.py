"""Contain functions to communicate with API and convert raw data"""
import json
from threading import Thread
from time import sleep
from typing import List

import requests

from app.app import db
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
    return data["results"]


def collect_more_users(number: int) -> None:
    """Add more users into database from API
    :param number: number of users to add
    :type number: `int`"""
    for i in range(5):
        try:
            json_users = get_users_json(number)
        except APIError:
            sleep(1 + i * i)
            continue
        else:
            break
    else:
        raise APIError  # TODO

    users = User.convert_into_users(json_users)
    from random_user_api import app

    with app.app_context():
        db.session.add_all(users)
        db.session.commit()


def collect_more_users_async(number: int) -> None:
    """Create thread and run in it collect_more_users
    :param number: number of users to add
    :type number: `int`"""
    get_users_task = Thread(
        target=collect_more_users,
        args=(number,),
        daemon=True,
    )
    get_users_task.start()
