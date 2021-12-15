import jwt
from datetime import datetime, timedelta
from Messages import app, db
from Messages.models import Message, User
from flask import request, jsonify
from Messages.auth import token_required


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
        return jsonify({'Error': 'User does not exist', 'authenticated': False}), 401

    token = jwt.encode(
        {
            'sub': user.username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        },
        app.config['SECRET_KEY']
    )

    return jsonify({'token': token})


@app.route('/api/post/message', methods=['POST'])
@token_required
def write_message(current_user):
    data = request.json
    message = Message(sender=current_user.username, receiver=data['receiver'], message=data['message'],
                      subject=data['subject'], date=datetime.utcnow())

    receiver = User.query.filter_by(username=data['receiver']).first()
    if not receiver:
        return {'Error': 'Receiver does not exist'}, 401

    db.session.add(message)
    db.session.commit()
    return jsonify(data)


@app.route('/api/get/messages', methods=['GET'])
@token_required
def get_all_messages(current_user):
    unread = request.args.get('unread')
    if unread is None:
        unread = False

    user = User.query.filter_by(username=current_user.username).first()

    if not user:
        return {'Error': 'User does not exist'}, 401

    messages = Message.query.filter_by(receiver=current_user.username, deleted_by_receiver=False)
    if unread:
        messages.filter_by(read=False)

    return jsonify([c.as_dict() for c in messages.all()])


@app.route('/api/get/message/<id>')
@token_required
def get_one_message(current_user, id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return {'Error': 'Message does not exist'}, 401

    if current_user.username != message.receiver:
        return {'Error': 'Not your message'}, 401

    message.read = True
    db.session.commit()

    return message.as_dict()


@app.route('/api/delete/<id>', methods=['POST'])
@token_required
def delete_message(current_user, id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return {'Error': 'Message does not exist'}, 401

    if message.sender == current_user.username:
        message.deleted_by_sender = True
        if message.deleted_by_receiver:
            db.session.delete(message)
        db.session.commit()
        return {'Ok': 'Deleted'}, 200
    elif message.receiver == current_user.username:
        message.deleted_by_receiver = True
        if message.deleted_by_sender:
            db.session.delete(message)
        db.session.commit()
        return {'Ok': 'Deleted'}, 200

    return {'Error': 'Not your message!'}, 401
