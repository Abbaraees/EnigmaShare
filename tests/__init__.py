import pytest

from app import create_app
from app.models import db, User

@pytest.fixture
def app():
    app = create_app(test_config={'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', 'SECRET_KEY': 'secret'})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user():
    user = User(username='user', email='user@mail.com')
    user.hash_password('password')
    db.session.add(user)
    db.session.commit()

    return user


