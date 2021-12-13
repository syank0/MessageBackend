import jwt
from datetime import datetime, timedelta
from Messages import app, db
from Messages.models import Message, User, ReceivedMessages
from flask import request, jsonify


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'Error': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode(
        {
            'sub': user.username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        },
        app.config['SECRET_KEY']
    )

    return jsonify({'token': str(token.encode('UTF-8'))})


@app.route('/api/get/<username>/messages', methods=['POST'])
def get_all_messages(username):
    unread = request.args.get('unread')
    if unread is None:
        unread = False

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'Error: User does not exist'}, 401

    messages = ReceivedMessages.query.with_parent(user).options(db.joinedload("message").joinedload("sender"))
    if unread:
        messages.filter_by(read=False)

    return jsonify(messages)


def write_message():
    data = request.json
    message = Message(sender=data['sender'], receiver=data['receiver'])
    db.session.add(message)
    db.session.commit()
    return jsonify(data)


@app.route('/messages', methods=['GET'])
def get_all_messages():
    messages = Message.query.all()
    return jsonify(messages)
