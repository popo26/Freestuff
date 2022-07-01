import os
from dotenv import load_dotenv


load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, "dev.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WHOOSH_BASE = "whoosh"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    APP_ADMIN = os.getenv("APP_ADMIN")
    APP_MAIL_SUBJECT_PREFIX = "FreeStuff - "
    APP_MAIL_SENDER = f"FreeStuff Admin <{APP_ADMIN}>"

    MSEARCH_INDEX_NAME = 'msearch'
    MSEARCH_BACKEND = 'whoosh'
    MSEARCH_PRIMARY_KEY = 'id'
    MSEARCH_ENABLE = True

    POSTS_PER_PAGE = 12  
   

    @staticmethod
    def init_app(ap):
        pass

config = {"default": Config}