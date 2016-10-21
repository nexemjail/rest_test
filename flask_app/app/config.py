import os
base_dir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'mother told me'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'app.db')
