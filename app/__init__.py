import os
from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate
from flask_msearch import Search
from sqlalchemy import MetaData



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
search = Search()

def create_app(config_name = "default"):
    app = Flask(__name__)
    
    migrate = Migrate(app, db, render_as_batch=True)
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    UPLOAD_FOLDER = "static/upload"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["UPLOADED_PHOTOS_DEST"] = "static/uploads"
    # app.configure_uploads(app, photos)
    # photos.init_app(app, photos)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    search.init_app(app)

    app.app_context().push()
   
   #When creating a new db below 3 lines need to be commented since it cannot access models
    from app.models import Post
    search.create_index(Post)
    # search.create_index(Post, update=True)
    # search.create_index(delete=True)
    # search.create_index(Post, delete=True)
    
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app