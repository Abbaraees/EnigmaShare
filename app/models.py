from app import db
from app import bcrypt


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    file = db.Column(db.String(100))
    encrypted = db.Column(db.Boolean)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return f"<Message: '{self.file}'"


class User(db.Model):
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
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"<User: {self.username}>"
