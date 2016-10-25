from app import login_manager, db, api
from flask_restful import Resource, marshal_with
from flask import request, session
import flask_login
from models import User
from utils import ResponseCodes


class ValidationError(Exception):
    pass


class Logout(Resource):
    @flask_login.login_required
    def get(self):
        flask_login.logout_user()
        session.update()
        return {'message': 'you are logged out'}, ResponseCodes.OK


def is_valid(data):
    username = data.get('username', None)
    password = data.get('password', None)

    if username is None or password is None:
        return True
    return True


class Login(Resource):
    def post(self):
        data = request.get_json()
        if not is_valid(data):
            return {'error': 'invalid data format'}, ResponseCodes.BAD_REQUEST_400
        else:
            user = User.query.filter_by(username=data['username'],
                                        password=data['password']).first()
            if not user:
                return {'error': 'invalid credentials'}, ResponseCodes.BAD_REQUEST_400

            if not flask_login.login_user(user):
                return {'error': 'error while logging in'}, ResponseCodes.SERVER_ERROR_500

            return {'message': 'you are logged in!'}, ResponseCodes.OK


class Register(Resource):
    def post(self):
        data = request.get_json()
        if not is_valid(data):
            return {'error': 'invalid data format'}, ResponseCodes.BAD_REQUEST_400

        users_found = User.query.filter_by(username=data['username']).count()
        if users_found > 0:
            return {'error': 'user already exists'}, ResponseCodes.BAD_REQUEST_400

        user = User(username=data['username'],
                    password=data['password'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'user successfully created'}, ResponseCodes.OK


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


class UserList(Resource):
    @flask_login.login_required
    def get(self, id):
        user = User.query.filter_by(id=id).first_or_404()
        return {'user': str(user)}, ResponseCodes.OK


api.add_resource(Register, '/register/')
api.add_resource(Login, '/login/')
api.add_resource(Logout, '/logout/')
api.add_resource(UserList, '/<int:id>/')
