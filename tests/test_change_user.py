from copy import deepcopy
from unittest.mock import MagicMock

import random_user_api
from app.business_logic import api_data
from app.business_logic.change_user import allowed_file, change_data, get_form_fields
from app.main.forms import ChangeUserDataForm
from tests.conftest import TEST_USERS


def test_allowed_file_positive(context):
    """Test that allowed file work correct"""
    assert allowed_file("file.jpg")


def test_allowed_file_negative(context):
    """Test that allowed file work correct"""
    assert not allowed_file("file")


def test_get_form_fields():
    """Test that form field generate right"""
    assert len(list(get_form_fields(ChangeUserDataForm))) == 10
