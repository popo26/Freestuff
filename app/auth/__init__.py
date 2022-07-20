from flask import Blueprint

auth = Blueprint('auth', __name__,
                    url_prefix="/auth/",
                    template_folder="templates",
                    static_folder="/static",
                    static_url_path="",
                    )

from . import views, errors