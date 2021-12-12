from werkzeug.security import generate_password_hash, check_password_hash

from Messages import db
from dataclasses import dataclass


@dataclass
class User(db.Model):
    __tablename__ = 'users'

    username: str
    password: str

    username = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(120), unique=True, nullable=False)

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


@dataclass
class Message(db.Model):
    __tablename__ = 'message'

    sender: str
    receiver: str

    sender = db.Column(db.Text(length=2), nullable=False, primary_key=True)
    receiver = db.Column(db.Text, nullable=False, primary_key=True)
    # message = db.column(db.String())
    # subject = db.Column(db.String(), nullable=False)
    # date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'sender: {self.sender}'
