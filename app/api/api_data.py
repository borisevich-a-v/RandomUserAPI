import aiohttp
import requests
import json

API_URL = 'https://randomuser.me/api'


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
	response = requests.get(API_URL,
	                        params={'results': user_number})
	if response.status_code != 200:
		raise BadAPIStatusCode(f'{API_URL} return {response.status_code}')
	print(response.text)
	return response.text


def convert_raw_json(raw_json: str, user_numbers: int) -> dict:
	"""Convert raw JSON to a list of a users"""
	try:
		data = json.loads(raw_json)
		if int(data['info']['results']) != user_numbers:
			raise BadRawJSON
	except ValueError:
		raise BadRawJSON
	except KeyError:
		raise BadRawJSON
	return data['results']


def get_users(number: int) -> dict:
	"""Return list of dicts. Each dict contains info about users"""
	return convert_raw_json(make_request(number), number)
