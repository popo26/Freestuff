from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp, Email
from .. models import User

class LoginForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        [validators.DataRequired()])
                                   
    username = StringField('Username', 
                            validators=[
                            DataRequired(),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                    'Usernames must have only letters, numbers, dots, or underscores',
                            )])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password_confirm', message='Passwords do not match.'
        )])
    password_confirm = PasswordField('Password (confirm):',
                                    [validators.DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry! Username already exists.")

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. Please register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password_confirm', message='Passwords do not match.'
        )])
    password_confirm = PasswordField('Password (confirm):',
                                    [validators.DataRequired()])
    submit = SubmitField("Reset Password")