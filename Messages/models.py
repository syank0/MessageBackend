from datetime import datetime
from typing import List

from werkzeug.security import generate_password_hash, check_password_hash

from Messages import db
from dataclasses import dataclass


@dataclass
class User(db.Model):
    __tablename__ = 'user'
    username: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    sent = db.relationship('Message', back_populates='sender')
    received = db.relationship('ReceivedMessages', back_populates='user_received', lazy=False)

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
    read: bool

    id = db.Column(db.Integer, primary_key=True)
    sender = db.relationship("User", back_populates="sent")
    receiver = db.relationship('ReceivedMessages', back_populates='message')
    message = db.column(db.String(120), unique=False, nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'sender: {self.sender}'


class ReceivedMessages(db.Model):
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    read = db.Column(db.Boolean, nullable=False, default=False)
    message = db.relationship('Message', back_populates='receiver')
    user_received = db.relationship('User', back_populates='received')
    messages = db.relationship('Message')
