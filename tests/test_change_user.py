import os
from pathlib import Path
from unittest.mock import Mock

from app.business_logic.change_user import (
    allowed_file,
    create_user,
    get_form_fields,
    next_portrait_file_name,
)
from app.main.forms import ChangeUserDataForm
from app.models import User


def test_allowed_file_positive(context):
    """Test that allowed file work correct"""
    assert allowed_file("file.jpg")


def test_allowed_file_negative(context):
    """Test that allowed file work correct"""
    assert not allowed_file("file")


def test_get_form_fields():
    """Test that form field generate right"""
    assert len(list(get_form_fields(ChangeUserDataForm))) == 10


def test_next_portrait_file_name():
    """Test next portrait file name work correct"""
    path = Path("app/static/portraits/large/")
    try:
        open(path / "9999998.jpg", "w")
        assert next_portrait_file_name(path) == "9999999.jpg"
    finally:
        os.remove(path / "9999998.jpg")


def test_create_user(context):
    """Test that user create"""
    mock = Mock()
    mock_with_data = Mock(data="1")
    for attribute in get_form_fields(ChangeUserDataForm):
        setattr(mock, attribute, mock_with_data)

    assert create_user(mock) == 1
    assert User.query.count() == 1
