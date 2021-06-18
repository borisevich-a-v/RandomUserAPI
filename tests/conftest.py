import pytest

from app.app import create_app, db

TEST_USERS = [
    {
        "gender": "male",
        "name": {"title": "Mr", "first": "Ray", "last": "Wright"},
        "email": "ray.wright@example.com",
        "phone": "017683 59191",
        "picture": {
            "large": "https://randomuser.me/api/portraits/men/72.jpg",
            "thumbnail": "https://randomuser.me/api/portraits/thumb/men/72.jpg",
        },
        "location": {
            "street": {"name": "New Street"},
            "city": "Liverpool",
            "state": "Mid Glamorgan",
            "country": "United Kingdom",
            "postcode": "M7 4TH",
        },
    },
    {
        "gender": "male",
        "name": {"title": "Mr", "first": "Allen", "last": "Carroll"},
        "location": {
            "street": {"name": "Highfield Road"},
            "city": "Armagh",
            "state": "Surrey",
            "country": "United Kingdom",
            "postcode": "UQ6S 4YF",
        },
        "email": "allen.carroll@example.com",
        "phone": "015395 25780",
        "picture": {
            "large": "https://randomuser.me/api/portraits/men/87.jpg",
            "thumbnail": "https://randomuser.me/api/portraits/thumb/men/87.jpg",
        },
    },
]


@pytest.fixture
def context():
    app = create_app("testing")
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield {"app": app, "db": db, "context": app_context}
    db.session.remove()
    db.drop_all()
    app_context.pop()


class FakeResponse:
    """Fake response for requests.get"""

    def __init__(self, status_code, text):
        """Constructor method"""
        self.status_code = status_code
        self.text = text
        self.ok = True if status_code < 400 else False


class FakeRequests:
    """Fake requests"""

    def __init__(self, status_code, text):
        """Constructor method"""
        self.response = FakeResponse(status_code, text)

    def get(self, *args, **kwargs):
        """Fake requests.get()"""
        return self.response
