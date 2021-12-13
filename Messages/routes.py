import jwt
from datetime import datetime, timedelta
from Messages import app, db
from Messages.models import Message, User
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


@app.route('/api/post/message', methods=['POST'])
def write_message():
    data = request.json
    message = Message(sender=data['sender'], receiver=data['receiver'], message=data['message'],
                      subject=data['subject'], date=datetime.utcnow())

    receiver = User.query.filter_by(username=data['receiver']).first()
    if not receiver:
        return {'Error': 'Receiver does not exist'}, 401

    db.session.add(message)
    db.session.commit()
    return jsonify(data)


@app.route('/api/get/<username>/messages', methods=['GET'])
def get_all_messages(username):
    unread = request.args.get('unread')
    if unread is None:
        unread = False

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'Error': 'User does not exist'}, 401

    messages = Message.query.filter_by(receiver=username)
    if unread:
        messages.filter_by(read=False)

    return jsonify([c.as_dict() for c in messages.all()])


@app.route('/api/get/<username>/message/<id>')
def get_one_message(username, id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return {'Error': 'Message does not exist'}, 401

    if username != message.receiver:
        return {'Error': 'Not your message'}

    message.read = True

    return message.as_dict()
