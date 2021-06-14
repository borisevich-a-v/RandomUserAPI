"""Test API"""
import pytest

from app.api import api_data


class FakeResponse:
    """Fake response for requests.get"""

    def __init__(self, status_code, text):
        """Constructor method"""
        self.status_code = status_code
        self.text = text


class FakeRequests:
    """Fake requests"""

    def __init__(self, status_code, text):
        """Constructor method"""
        self.response = FakeResponse(status_code, text)

    def get(self, *args, **kwargs):
        """Fake requests.get()"""
        return self.response


def test_bad_status_code(monkeypatch):
    """Test bad response status code"""
    monkeypatch.setattr(api_data, "requests", FakeRequests(404, "a"))

    with pytest.raises(api_data.BadAPIResponse):
	    api_data.make_request_users(1)


def test_bad_json():
    """Test if we get bad json"""
    response = FakeResponse(200, "not a json")
    with pytest.raises(api_data.BadRawJSON):
	    api_data.get_users_json(response.text)


def test_positive_api(monkeypatch):
    """Test if all is ok"""
    json_test = """{"results":{"is_json":true},"info":{"results":1}}"""
    monkeypatch.setattr(api_data, "requests", FakeRequests(200, json_test))
    users = api_data.get_users(1)
    assert users == {"is_json": True}
