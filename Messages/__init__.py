from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message.db'
app.config['SECRET_KEY'] = '2ae11bb893aab97bb1a29d88'
db = SQLAlchemy(app)

from Messages import models

db.init_app(app)
with app.app_context():
    db.drop_all()

from Messages import routes
from Messages import auth