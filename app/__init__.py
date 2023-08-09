from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from config import Config


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object(Config)

    # initialiaze extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    @app.route('/test')
    def test():
        return '<h1>Test</h1>'
    

    return app

from app import models