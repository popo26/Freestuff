import os
from flask import Flask
# from app.models import Post
from config import config
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate, upgrade
# from flask_msearch import Search
from sqlalchemy import MetaData
from flask_wtf.csrf import CSRFProtect
import boto3
from datetime import timedelta



load_dotenv()

#for migration issue
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


bootstrap=Bootstrap()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login first."
login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = "You need to login again."
# search = Search()
csrf = CSRFProtect()
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


def create_app(config_name = "default"):
    app = Flask(__name__)
    
    # migrate = Migrate(app, db, render_as_batch=True) For SQLite
    migrate = Migrate(app, db)
        
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
   
    UPLOAD_FOLDER = "static/uploads"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['S3_BUCKET_NAME'] = os.getenv('S3_BUCKET_NAME')
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(seconds=21600) #6hours RememberMe not working yet
    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=21600)
    
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    with app.app_context():
        db.create_all()
   
                
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    if app.config['HTTPS_REDIRECT']:
        from flask_talisman import Talisman
        Talisman(app, content_security_policy={
                'default-src': [
                    "'self'",
                    'cdnjs.cloudflare.com',
                ],
                # allow images from anywhere, 
                #   including unicornify.pictures
                'img-src': '*'
            }
        )
    
    from flask_migrate import upgrade

    #Not working at the moment
    @app.cli.command()
    def deploy():
        """ Run deployment tasks """
        # migrate database
        
        upgrade()
        
        from app.models import Role
        Role.insert_roles()

    return app


def current_app(config_name="testing"):
    app = Flask(__name__)
    
    migrate = Migrate(app, db, render_as_batch=True)
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    UPLOAD_FOLDER = "static/upload"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["UPLOADED_PHOTOS_DEST"] = "static/uploads"
  
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    app.app_context().push()
    
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app