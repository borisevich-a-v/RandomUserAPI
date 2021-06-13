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
	for user_data in jsons_dict:
		user = User(
			gender=user_data["gender"],
			email=user_data['email'],
			phone=user_data['phone'],
			cell=user_data['cell'],
			nat=user_data['nat'],
			# Name
			title=user_data['name']['title'],
			first_name=user_data["name"]["first"],
			last_name=user_data["name"]["last"],
			# Location
			street_number=user_data['location']['street']['number'],
			street_name=user_data['location']['street']['name'],
			city=user_data["location"]["city"],
			state=user_data['location']['state'],
			country=user_data['location']['country'],
			postcode=user_data['location']['postcode'],
			latitude=user_data['location']['coordinates']['latitude'],
			longitude=user_data['location']['coordinates']['longitude'],
			timezone_offset=user_data['location']['timezone']['offset'],
			timezone_description=user_data['location']['timezone']['description'],
			# Login
			uuid=user_data['login']['uuid'],
			username=user_data['login']['username'],
			password=user_data['login']['password'],
			salt=user_data['login']['salt'],
			md5=user_data['login']['md5'],
			sha1=user_data['login']['sha1'],
			sha256=user_data['login']['sha256'],
			# Date of birth
			date_of_birth=user_data['dob']['date'],
			age=user_data['dob']['age'],
			# registered
			registered_date=user_data['registered']['date'],
			registered_age=user_data['registered']['age'],
			# id
			id_name=user_data['id']['name'],
			id_value=user_data['id']['value'],
			# Pictures
			picture_l=user_data['picture']['large'],
			picture_m=user_data['picture']['medium'],
			picture_s=user_data['picture']['thumbnail'],
		)
		users.append(user)
	return users


def get_more_users(number: int) -> List[User]:
	"""Return list of dicts. Each dict contains info about users"""
	users = convert_into_users(convert_raw_json(make_request(number), number))
	db.create_all()
	db.session.add_all(users)
	db.session.commit()
	return users
