# models.py
from sampling import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, current_user
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import sqlalchemy_utils
from flask import redirect, url_for, session, request


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    htmls = db.relationship('Html', backref='author',
                            lazy=True, cascade="all, delete, delete-orphan")

    def __init__(self, username, password):        
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'Username: {self.username};'

class Html(db.Model):
    __tablename__ = 'htmls'
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    html_key = db.Column(db.String(64), nullable=False)
    html = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, html_key, html, user_id):
        self.html_key = html_key
        self.html = html
        self.user_id = user_id        

    def __repr__(self):
        return "HTML ID: {  } -- Date: {  } --- {  } ".format(self.id, self.date, self.html_key)

