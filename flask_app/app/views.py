from app import app, login_manager, db, api
from flask_restful import Resource, Api
from flask import request, Blueprint, session
from models import User, Session
import flask_login


@flask_login.login_required
def logout():
    flask_login.logout_user()
    return {'message': 'you are logged out'}


class Logout(Resource):
    @flask_login.login_required
    def get(self):
        flask_login.logout_user()
        return {'message': 'you are logged out'}, 200


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


class Login(Resource):
    def post(self):
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if not username or not password:
            return {'error': 'invalid data format'}
        else:
            try:
                user = User.query.filter_by(username=username, password=password).first()
                # print user
            except Exception as e:
                return {'error': 'user not found'}, 404
            # print user
            if user:
                if not flask_login.login_user(user):
                    return {'error': 'error while logging in'}, 304
                # session_id = session['_id']

                # db.session.add(Session(id=session_id, user=user))
                # db.session.commit()
                return {'message': 'you are logged in!'}, 200
            return {'error': 'invalid credentials'}, 401




@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


class Register(Resource):
    def post(self):
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if not username or not password:
            return {'error': 'invalid data format'}, 404

        q = User.query.filter_by(username=username).count()
        if q:
            return {'error': 'user already exists'}, 401
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return {'message': 'user successfilly created'}, 200


api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


@app.route('/')
@flask_login.login_required
def index():
    return 'Allah'