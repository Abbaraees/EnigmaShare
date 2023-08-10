from app import db
from app.models import User, Message
from tests import app

def test_user_password_hashing():
    user = User(username='testuser', email='test@example.com')
    password = 'testpassword'
    user.hash_password(password)
    
    assert user.password_hash is not None
    assert user.password_hash != password

    assert user.check_password(password) is True
    assert user.check_password('wrongpassword') is False

def test_message_creation(app):
    with app.app_context():
        sender = User(username='sender', email='sender@example.com')
        receiver = User(username='receiver', email='receiver@example.com')
        receiver.hash_password("password")
        sender.hash_password("password")
        db.session.add(sender)
        db.session.add(receiver)
        db.session.commit()

        message = Message(file='test.txt', sender_id=sender.id, receiver_id=receiver.id)
        db.session.add(message)
        db.session.commit()

        assert message.id is not None
        assert message.file == 'test.txt'
        assert message.sender == sender
        assert message.receiver == receiver

def test_user_relationships(app):
    user = User(username='user', email='user@example.com')
    user.hash_password("password")
    db.session.add(user)
    db.session.commit()

    message_sent = Message(file='sent.txt', sender_id=user.id, receiver_id=user.id)
    message_received = Message(file='received.txt', sender_id=user.id, receiver_id=user.id)
    db.session.add(message_sent)
    db.session.add(message_received)
    db.session.commit()

    assert message_sent.sender == user
    assert message_received.receiver == user
