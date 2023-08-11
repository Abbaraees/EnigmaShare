from app import db
from app import bcrypt
from flask_login import UserMixin
from sqlalchemy import or_

from app import login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(255), nullable=False)
    file = db.Column(db.String(100))
    encrypted = db.Column(db.Boolean)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Message: '{self.file}'"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    sent_messages = db.relationship('Message',
        primaryjoin=(Message.sender_id==id),
        backref='sender',
        lazy=True
    )

    received_messages = db.relationship('Message',
        primaryjoin=(Message.receiver_id==id),
        backref='receiver',
        lazy=True
    )

    def hash_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_messages(self):
        return Message.query.filter(
           or_(Message.sender == self, Message.receiver == self)
        ).all()

    def __repr__(self):
        return f"<User: {self.username}>"
