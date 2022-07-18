from flask import Flask
from app import create_app, db
import os
from app.models import User


app = create_app('default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
