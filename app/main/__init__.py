from flask import Blueprint
from app.models import Category, Permission


main = Blueprint('main', 
                  __name__,
                  static_folder="/static",
                  static_url_path=""
                )

from . import views, errors



@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

def inject_categories():
    return dict(Category=Category)