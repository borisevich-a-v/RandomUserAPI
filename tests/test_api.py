"""Test API"""
import json
from copy import deepcopy
from unittest.mock import MagicMock

import pytest

import random_user_api
from app import api_data
from app.models import User
from tests.conftest import TEST_USERS, FakeRequests


def test_bad_status_code(monkeypatch):
    """Test bad response status code"""
    monkeypatch.setattr(api_data, "requests", FakeRequests(401, "a"))

    with pytest.raises(api_data.BadAPIResponse):
        api_data.get_users_json(1)


def test_bad_json(monkeypatch):
    """Test if we get bad json"""
    monkeypatch.setattr(api_data, "requests", FakeRequests(200, "a"))
    with pytest.raises(api_data.BadRawJSON):
        api_data.get_users_json(1)


def test_get_user_json_positive(monkeypatch):
    """Test that get and convert data from internet correct"""
    fake_api_json = json.dumps(
        {"info": {"results": 1}, "results": [deepcopy(TEST_USERS[0])]}
    )

    monkeypatch.setattr(api_data, "requests", FakeRequests(200, fake_api_json))
    result = api_data.get_users_json(1)
    assert len(result) == 1
    assert result[0]["gender"] == "male"
    assert result[0]["location"]["city"] == "Liverpool"


def test_collect_more_users(context):
    """Test that collect more users add users into database"""
    fake_users_json = [deepcopy(TEST_USERS[0])]
    api_data.get_users_json = MagicMock(return_value=fake_users_json)
    random_user_api.app.app_context = MagicMock(
        return_value=context["app"].app_context()
    )
    api_data.collect_more_users(1)
    count = User.query.count()
    assert count == 1
