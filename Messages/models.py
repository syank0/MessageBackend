from Messages import db


class Message(db.Model):
    __tablename__ = 'message'
    sender = db.Column(db.String(), nullable=False, primary_key=True)
    # receiver = db.Column(db.String(), nullable=False)
    # message = db.column(db.String())
    # subject = db.Column(db.String(), nullable=False)
    # date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
