"""Contain functions to communicate with API and convert raw data"""
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

import requests
from requests import Response

from app import db
from app.models import User

API_URL = "https://randomuser.me/api"


class APIError(Exception):
	"""General API error"""

	...


class BadAPIResponse(APIError):
	"""Raised when API's response is bad"""

	...


class BadRawJSON(APIError):
	"""Return wrong number of people"""

	...


def _download_one_portrait(json_dict):
	photo_number = get_portrait_id(json_dict)

	for size in ("large", "medium", "thumbnail"):
		path = Path(
			f"app/static/portraits/{size}/{photo_number}.jpg")
		if os.path.exists(path):
			continue
		response = requests.get(json_dict["picture"][size])
		if not response.ok:
			raise BadAPIResponse(f"{API_URL} status code {response.status_code}")
		with open(path, "wb") as handler:
			handler.write(response.content)


def download_portraits(data):
	with ThreadPoolExecutor(max_workers=len(data)) as pool:
		pool.map(_download_one_portrait, data)


def get_portrait_id(json_dict):
	"""Download photos if photo doesn't exist locally"""
	gender = 0 if json_dict["gender"] == "male" else 1
	photo_number = re.search(
		r"(\d{1,2})\.jpg$", json_dict["picture"]["large"]
	).group(1)
	return int(photo_number) + gender * 1000


def get_users_json(user_number: int) -> dict:
	"""Convert raw JSON to a list of a users"""
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


def convert_into_users(jsons_dict: dict) -> List[User]:
	"""Convert specific JSON into User"""
	users = []
	for user_data in jsons_dict:
		user = User(
			gender=user_data["gender"],
			email=user_data["email"],
			phone=user_data["phone"],
			# cell=user_data["cell"],
			# nat=user_data["nat"],
			# Name
			# title=user_data["name"]["title"],
			first_name=user_data["name"]["first"],
			last_name=user_data["name"]["last"],
			# Location
			# street_number=user_data["location"]["street"]["number"],
			street_name=user_data["location"]["street"]["name"],
			city=user_data["location"]["city"],
			state=user_data["location"]["state"],
			country=user_data["location"]["country"],
			postcode=user_data["location"]["postcode"],
			# latitude=user_data["location"]["coordinates"]["latitude"],
			# longitude=user_data["location"]["coordinates"]["longitude"],
			# timezone_offset=user_data["location"]["timezone"]["offset"],
			# timezone_description=user_data["location"]["timezone"]["description"],
			# Login
			# uuid=user_data["login"]["uuid"],
			# username=user_data["login"]["username"],
			# password=user_data["login"]["password"],
			# salt=user_data["login"]["salt"],
			# md5=user_data["login"]["md5"],
			# sha1=user_data["login"]["sha1"],
			# sha256=user_data["login"]["sha256"],
			# Date of birth
			# date_of_birth=user_data["dob"]["date"],
			# age=user_data["dob"]["age"],
			# registered
			# registered_date=user_data["registered"]["date"],
			# registered_age=user_data["registered"]["age"],
			# id
			# id_name=user_data["id"]["name"],
			# id_value=user_data["id"]["value"],
			# Pictures
			portrait_large=user_data["picture"]["large"],
			# portrait_medium=user_data["picture"]["medium"],
			portrait_thumbnail=user_data["picture"]["thumbnail"],

		)
		users.append(user)
	# download_portraits(jsons_dict)
	return users


def get_more_users(number: int) -> List[User]:
	"""Return list of dicts. Each dict contains info about users"""
	users = convert_into_users(get_users_json(number))
	db.create_all()
	db.session.add_all(users)
	db.session.commit()
	return users
