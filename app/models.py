from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    sex = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String(16))
    email = db.Column(db.String)
    location = db.Column(db.String)
    photo = db.Column(db.String)


def get_users(number=1):
    user1 = User(
        id=1,
        first_name="Zhou",
        last_name="Xin",
        phone="89313541299",
        email="ZhouX@mail.ru",
        location="Spb Nevskiy, 21",
        photo="Photo",
    )

    user2 = User(
        id=1,
        first_name="Andrey",
        last_name="Borisevich",
        phone="8934576299",
        email="AndreyB@gmail.com",
        location="Spb Nevskiy, 21",
        photo="Photo2",
    )

    users = [user1, user2]
    print(users[:number])
    return users[:number]


get_users(3)
