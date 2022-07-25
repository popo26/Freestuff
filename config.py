import os
from dotenv import load_dotenv
import psycopg2
import boto3

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.getenv("SECRET_KEY")
    #.replace for heroku deployment
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
    # or 'sqlite:///' + os.path.join(basedir, "dev.sqlite")
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # or 'sqlite:///' + os.path.join(basedir, "dev.sqlite")
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # WHOOSH_BASE = "whoosh" #For flask-msearch

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    APP_ADMIN = os.getenv("APP_ADMIN")
    APP_MAIL_SUBJECT_PREFIX = "FreeStuff - "
    APP_MAIL_SENDER = f"FreeStuff Admin <{APP_ADMIN}>"
      
    POSTS_PER_PAGE = 12  

    UPLOAD_FOLDER = os.getenv('S3_BUCKET_PATH')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    HTTPS_REDIRECT = False

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    ACL = 'public-read'
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    S3_REGION = os.getenv('S3_REGION') 
    S3_BUCKET_PATH = os.getenv('S3_BUCKET_PATH')
   

    @staticmethod
    def init_app(ap):
        pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') or \
        'sqlite:///' + os.path.join(basedir, "test.sqlite")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "data.sqlite")}'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        creds = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            creds = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                # logging: to use TLS, must pass tuple (can be empty)
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.APP_MAIL_SENDER,
            toaddrs=[cls.APP_ADMIN],
            subject=cls.APP_MAIL_SUBJECT_PREFIX + " Application Error",
            credentials=creds,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

   


class HerokuConfig(ProductionConfig):
    HTTPS_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler
        file_handler.setLevel(file_handler, level=logging.INFO)
        app.logger.addHandler(file_handler)

        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
    
   


config = {
    "default": Config,
    'testing': TestingConfig,
    'heroku': HerokuConfig,
    }