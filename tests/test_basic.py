from flask import current_app


def test_app_exists(context):
    """Test that fixture work correct"""
    assert current_app is not None


def test_app_is_testing(context):
    """Test that we use testing mode"""
    assert current_app.config["TESTING"]
