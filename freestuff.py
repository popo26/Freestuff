from flask import Flask
from app import create_app, db
import os
from app.models import User
# from flask_migrate import Migrate

app = create_app('default')
# migrate = Migrate(app, db, render_as_batch=True) 

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
