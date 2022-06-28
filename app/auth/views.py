
from flask import render_template, redirect, url_for, flash, request
import datetime
from . import auth
import smtplib
import os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Mail, Message
from app import mail
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, logout_user, current_user
from app.models import User
from ..import db, login_manager
from ..email import send_email


s = URLSafeTimedSerializer(os.getenv('DANGEROUS_SECRET'))
YEAR = datetime.datetime.now().year

@auth.route('/login', methods=["GET", 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email_entered = form.email.data
        user = User.query.filter_by(email=email_entered).first()
        remember_me = True if request.form.get("remember_me") else False
        
        if not user:
            flash("User info can't be found. Please register first.")
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember_me)
        next = request.args.get("next")

        if next is None or not next.startswith("/"):
            next = url_for('main.index')
        return redirect(next)

    return render_template("auth/login.html", form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        email = request.form['email']
        token = s.dumps(email, salt=os.getenv("SALTIES"))
        link = url_for('auth.confirm', token=token, _external=True)
        html = render_template('mail/confirm.html', link=link)
        send_email(user.email, "Please confirm the link below.", html)

        return redirect(url_for('auth.unconfirmed'))

    return render_template("auth/register.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out. Good Bye!")
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed\
            and request.endpoint \
            and request.blueprint != 'auth'\
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/confirm/<token>')
def confirm(token):
    try:
        email=s.loads(token, salt=os.getenv("SALTIES"), max_age=180)
    except SignatureExpired:
        return "The token is expired"
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash("Account already confirmed before. Go to Login screen.")
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        send_email(user.email, "Welcome to FreeStuff!", 'mail/user_welcome.html', user=user)
        send_email(os.getenv('MAIL_USERNAME'), f"Notification: A new user({user.username}) is added", 'mail/admin_new_user.html', user=user)
        flash("Now you can login now!")
    return redirect(url_for('auth.login'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route("/confirm")
def resend_confirmation():
    token = s.dumps(current_user.email, salt=os.getenv("SALTIES"))
    link = url_for('auth.confirm', token=token, _external=True)
    html = render_template('mail/confirm.html', link=link)
    send_email(current_user.email, "Reconfirm link sent below.", html)
    flash("Confirmation link has been resent, Please check your mailbox.")
    return redirect(url_for('auth.unconfirmed'))
                


