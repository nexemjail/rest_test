import flask_login
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api

import config

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
api = Api(app)

from app import models, views

db.create_all()