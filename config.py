import os

BASE_DIR = os.path.dirname(__file__)

class Config(object):
    SECRET_KEY = '6nfi30l.930dlpnu92w/.e-dwygo2nsqy;o1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.sqlite'
    UPLOADS_DIR = BASE_DIR + '/app/static/uploads'