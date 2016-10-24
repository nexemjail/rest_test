from app import login_manager, db, api
from flask_restful import Resource
from flask import request, session
import flask_login
from models import User
from utils import ResponseCodes


class Logout(Resource):
    @flask_login.login_required
    def get(self):
        flask_login.logout_user()
        session.update()
        return {'message': 'you are logged out'}, ResponseCodes.OK


class Login(Resource):
    def post(self):
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if not username or not password:
            return {'error': 'invalid data format'}, ResponseCodes.BAD_REQUEST_400
        else:
            user = User.query.filter_by(username=username, password=password).first()
            if not user:
                return {'error': 'invalid credentials'}, ResponseCodes.BAD_REQUEST_400

            if not flask_login.login_user(user):
                return {'error': 'error while logging in'}, ResponseCodes.SERVER_ERROR_500

            return {'message': 'you are logged in!'}, ResponseCodes.OK


class Register(Resource):
    def post(self):
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if not username or not password:
            return {'error': 'invalid data format'}, ResponseCodes.BAD_REQUEST_400

        q = User.query.filter_by(username=username).count()
        if q > 0:
            return {'error': 'user already exists'}, ResponseCodes.BAD_REQUEST_400

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return {'message': 'user successfully created'}, ResponseCodes.OK


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


class UserList(Resource):
    @flask_login.login_required
    def get(self):
        return {'users': map(lambda x: x.username, User.query.all())}, ResponseCodes.OK

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(UserList, '/')
