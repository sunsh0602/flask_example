from toy import db, bcrypt
from toy.common.exceptions import CustomException
from toy.models.example_models import ExampleUser, User


# class ExampleDAO(object):
#     def __init__(self):
#         pass
#
#     def get(self, name: str) -> str:
#         return ExampleUser.query.filter_by(name=name).first()
#
#     def create(self, name: str):
#         user = ExampleUser(name=name)
#         db.session.add(user)
#         db.session.commit()

class ExampleDAO(object):
    def __init__(self):
        pass

    def get(self, name: str) -> str:
        user = ExampleUser.query.filter_by(name=name).first()
        if user is None:
            print("여기네")
            raise CustomException()
        return user.name

    def create(self, name: str):
        user = ExampleUser(name=name)
        db.session.add(user)
        db.session.commit()


class ExampleSignDAO(object):
    def __init__(self):
        pass

    def get(self, user_id: str, password: str) -> None:
        user = User.query.filter_by(user_id=user_id).one_or_none()
        if not user or not bcrypt.check_password_hash(pw_hash=user.password, password=password):
            raise CustomException()

    def create(self, user_id: str, password: str):
        if User.query.filter_by(user_id=user_id).one_or_none():
            raise CustomException()
        user = User(user_id=user_id, password=password)
        db.session.add(user)
        db.session.commit()


class ExampleRefreshDAO(object):
    def __init__(self):
        pass

    def get(self, user_id: str) -> str:
        return User.query.filter_by(user_id=user_id).one_or_none()