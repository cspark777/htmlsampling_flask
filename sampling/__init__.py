#sampling/__init__.py

import os

from flask_dance.contrib.google import make_google_blueprint, google
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
import sqlalchemy_utils


basedir = os.path.abspath(os.path.dirname(__file__))

static_path = basedir + "/static/"

app = Flask(__name__, static_url_path='', static_folder=static_path)

app.config['SECRET_KEY'] = 'myscecret'

##################
####Database Setup
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

##################
####Login Config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

##################

from sampling.users.views import users
from sampling.error_pages.handler import error_pages
from sampling.page.views import page

app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(page)
