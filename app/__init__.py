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


load_dotenv()

bootstrap=Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app(config_name = "default"):
    app = Flask(__name__)

    migrate = Migrate(app, db, render_as_batch=True)
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app