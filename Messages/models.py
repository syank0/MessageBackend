from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from Messages import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def as_dict(self):
        user_dict = {}
        for c in self.__table__.columns:
            user_dict[c.name] = getattr(self, c.name)
        return user_dict


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), unique=False, nullable=False)
    receiver = db.Column(db.String(120), unique=False, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, unique=False, default=False)
    deleted_by_sender = db.Column(db.Boolean, unique=False, default=False)
    deleted_by_receiver = db.Column(db.Boolean, unique=False, default=False)

    def as_dict(self):
        message_dict = {}
        for c in self.__table__.columns:
            if c.name != 'read' and c.name != 'deleted_by_sender' and c.name != 'deleted_by_receiver':
                message_dict[c.name] = getattr(self, c.name)
        return message_dict
