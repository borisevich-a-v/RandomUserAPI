"""Test validators for forms"""
from unittest.mock import Mock

import pytest
from wtforms import ValidationError

from app.main.forms import check_phone


def test_short_phone():
    """Test that exception raise when phone is too short"""
    phone = Mock(data="+7-931-222-23")

    with pytest.raises(ValidationError):
        check_phone("", phone)


def test_long_phone():
    """Test that exception raise when phone is too long"""
    phone = Mock(data="+7-931-222-23-55-21")

    with pytest.raises(ValidationError):
        check_phone("", phone)


def test_phone_contains_letter():
    """Test that exception raise when phone contains"""
    phone = Mock(data="+7-931-22c-55-01")

    with pytest.raises(ValidationError):
        check_phone("", phone)


def test_phone_positive():
    """Test that exception raise when phone contains"""
    phone = Mock(data="+7-931-222-55-01")
    check_phone("", phone)
