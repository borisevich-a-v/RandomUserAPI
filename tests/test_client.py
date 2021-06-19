"""Test that pages correct"""
import os
from copy import deepcopy
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import random_user_api
from app.business_logic import api_data
from app.business_logic.change_user import next_portrait_file_name
from app.models import User
from tests.conftest import TEST_USERS


@pytest.fixture
def ext_context(context):
    """Add client into context"""
    context["app"].config["WTF_CSRF_ENABLED"] = False
    context["client"] = context["app"].test_client()
    yield context


def test_404(ext_context):
    """Test when route not found"""
    response = ext_context["client"].get("/wrong/url")
    assert response.status_code == 404
    assert "<h1>Not Found</h1>" in response.get_data(as_text=True)


def test_main_table(ext_context):
    """Test table on main page is built correctly"""
    # Add user
    fake_users_json = deepcopy(TEST_USERS)
    api_data.get_users_json = MagicMock(return_value=fake_users_json)
    random_user_api.app.app_context = MagicMock(
        return_value=ext_context["app"].app_context()
    )
    api_data.collect_more_users(1)
    response = ext_context["client"].get("/")
    assert response.status_code == 200
    response = response.get_data(as_text=True)
    assert "<tbody>" in response
    assert "<td>017683 59191</td>" in response


def test_user_page(ext_context):
    """Test user page"""
    # Add user
    fake_users_json = deepcopy(TEST_USERS)
    api_data.get_users_json = MagicMock(return_value=fake_users_json)
    random_user_api.app.app_context = MagicMock(
        return_value=ext_context["app"].app_context()
    )
    api_data.collect_more_users(2)
    response = ext_context["client"].get("/1")
    assert response.status_code == 200
    response = response.get_data(as_text=True)
    assert "1. Ray Wright" in response


def test_change_user_data(ext_context):
    """Test change user data works"""
    # Add user
    fake_users_json = deepcopy(TEST_USERS)
    api_data.get_users_json = MagicMock(return_value=fake_users_json)
    random_user_api.app.app_context = MagicMock(
        return_value=ext_context["app"].app_context()
    )
    api_data.collect_more_users(2)

    # Change user 1
    test_data = {
        "gender": "male",
        "email": "realmail@example.com",
        "phone": "+1 111 111 11 11",
        "first_name": "e",
        "last_name": "e",
        "street_name": "e",
        "city": "e",
        "state": "e",
        "country": "e",
        "postcode": "e",
    }
    response = ext_context["client"].post("/1/change_data", data=test_data)

    assert response.status_code < 400

    user = User.query.get(1)
    assert user.gender == test_data["gender"]
    assert user.email == test_data["email"]
    assert user.phone == test_data["phone"]
    assert user.first_name == test_data["first_name"]
    assert user.last_name == test_data["last_name"]
    assert user.street_name == test_data["street_name"]
    assert user.city == test_data["city"]
    assert user.state == test_data["state"]
    assert user.country == test_data["country"]
    assert user.postcode == test_data["postcode"]


def check_change_user_portrait(photo, context, path_l, path_t):
    """Test change user portrait"""
    # Add user
    fake_users_json = deepcopy(TEST_USERS)
    api_data.get_users_json = MagicMock(return_value=fake_users_json)
    random_user_api.app.app_context = MagicMock(
        return_value=context["app"].app_context()
    )
    api_data.collect_more_users(2)
    # Create post's data
    data = {
        "name": "this is a name",
    }
    data = {key: str(value) for key, value in data.items()}
    data["file"] = (photo, "test.jpg")

    response = context["client"].post(
        "/1/change_portrait",
        data=data,
        follow_redirects=True,
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    assert os.path.exists(path_l)
    assert os.path.exists(path_t)
    user = User.query.get(1)
    assert path_l == Path("app/" + user.portrait_large)
    assert path_t == Path("app/" + user.portrait_thumbnail)


def test_change_user_portrait(ext_context):
    """Test change user portrait"""
    next_file_name = next_portrait_file_name(Path("app/static/portraits/large"))
    path_l = Path("app/static/portraits/large", next_file_name)
    path_t = Path("app/static/portraits/thumbnail", next_file_name)
    with open(Path("tests/assist_files/test_portrait.jpg"), "br") as photo:
        try:
            check_change_user_portrait(photo, ext_context, path_l, path_t)
        finally:
            os.remove(path_l)
            os.remove(path_t)


def test_create_new_user(ext_context):
    """Test that new user created correct"""
    test_data = {
        "gender": "male",
        "email": "realmail@example.com",
        "phone": "+1 111 111 11 11",
        "first_name": "e",
        "last_name": "e",
        "street_name": "e",
        "city": "e",
        "state": "e",
        "country": "e",
        "postcode": "e",
    }
    response = ext_context["client"].post("/new_user", data=test_data)

    assert response.status_code < 400

    user = User.query.get(1)
    assert user.gender == test_data["gender"]
    assert user.email == test_data["email"]
    assert user.phone == test_data["phone"]
    assert user.first_name == test_data["first_name"]
    assert user.last_name == test_data["last_name"]
    assert user.street_name == test_data["street_name"]
    assert user.city == test_data["city"]
    assert user.state == test_data["state"]
    assert user.country == test_data["country"]
    assert user.postcode == test_data["postcode"]
