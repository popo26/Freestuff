from tokenize import String
from typing import Text
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, MultipleFileField
from app.models import Category
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp, Length, Email
from .. models import User
from flask_login import current_user

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0,64)])
    username = StringField("Username", validators=[Length(0,64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[Length(0,64)])
    bio = TextAreaField("Bio")
    submit = SubmitField("Submit")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Sorry! the username is taken. Please choose different one.')

    def validate_email(self, email):
        if email.data!= current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists.")

class AdminLevelEditProfileForm(FlaskForm):
    username = StringField("Username", validators=[Length(0,64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    confirmed = BooleanField("Confirmed User?")
    role = SelectField("Role", coerce=int, choices=[(1, 'User'), (2, 'Administrator')]) #deal with it later
    name = StringField("Name", validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    bio = TextAreaField("Bio")
    submit = SubmitField("Submit")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Sorry! the username is taken. Please choose different one.')

    def validate_email(self, email):
        if email.data!= current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already exists.")

class PostForm(FlaskForm):
    category = SelectField("Category", coerce=int, default=False, validators=[DataRequired()])
    photos = FileField("Photos", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'pdf'])])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField("Tell us about your free stuff", render_kw={'rows':'10'})
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [
            (Category.HOME_LIVING, 'Home&Living'),
            (Category.KITCHEN, 'Kitchen'),
            (Category.BABY, 'Baby'),
            (Category.BOOKS, 'Books'),
            (Category.CRAFT, 'Craft'),
            (Category.ELECTRONICS, 'Electronics'),
            (Category.PETS, 'Pets'),
            (Category.CLOTHING, 'Clothing'),
            (Category.BATHROOM, 'Bathroom'),
            (Category.TOYS, 'Toys'),
            (Category.JEWELLERY, 'Jewellery'),
        ]


class ContactGiverForm(FlaskForm):
    description = TextAreaField("Any message or inquiry goes here.", validators=[DataRequired()], render_kw={'rows':'10'})
    submit = SubmitField("Submit")

class ReplyForm(FlaskForm):
    description = TextAreaField('Reply', validators=[DataRequired()], render_kw={'rows':'10'})
    submit = SubmitField("Reply")