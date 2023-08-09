from flask import Flask

from config import Config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object(Config)


    @app.route('/test')
    def test():
        return '<h1>Test</h1>'
    

    return app
