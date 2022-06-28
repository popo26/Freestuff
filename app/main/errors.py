from flask import render_template
from . import main

@main.app_errorhandler(403) #change app.errorhandler to main.app_errorhandler so this error handlers can handle errors globally
def forbidden(e):
    error_title = "Forbidden"
    error_msg = "You shouldn't be here!"
    return render_template('error.html', 
                            error_title=error_title,
                            error_msg=error_msg), 403

@main.app_errorhandler(404)
def page_not_found(e):
    error_title = "Not Found"
    error_msg = "That page does not exist"
    return render_template('error.html', 
                            error_title=error_title,
                            error_msg=error_msg), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    error_title = "Internal Server Error"
    error_msg = "Sorry, we see mto be experiencing server issue"
    return render_template('error.html', 
                            error_title=error_title,
                            error_msg=error_msg), 500