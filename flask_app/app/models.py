from app import db
from flask_login import UserMixin

USER_ROLE = 0
ADMIN_ROLE = 1


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.Boolean, default=USER_ROLE)

    def __repr__(self):
        return '{}: {}'.format(self.id, self.username)

    def __str__(self):
        return self.__repr__()
