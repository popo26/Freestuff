from flask import current_app, render_template
from flask_mail import Message
from . import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):

    app = current_app._get_current_object()

    msg = Message(
        subject=current_app.config["APP_MAIL_SUBJECT_PREFIX"] + subject,
        recipients = [to],
        html=template,
        sender=current_app.config['APP_MAIL_SENDER']
    )

    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()

    mail.send(msg)
