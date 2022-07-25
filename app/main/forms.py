from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from app.models import Category
from wtforms.validators import DataRequired, ValidationError, Length, Email
from .. models import User
from flask_login import current_user, login_user
from app import db


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
    role = SelectField("Role", coerce=int, choices=[(1, 'User'), (2, 'Administrator')])
    name = StringField("Name", validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    bio = TextAreaField("Bio")
    submit = SubmitField("Submit")

    #Without overwriting, the existing username is marked as already exists.
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(AdminLevelEditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.query(User).filter_by(
                username=self.username.data).first()
            if user is not None:
                raise ValidationError('Sorry! Username already exists.')
               
    def validate_email(self, email):
        if email.data != self.original_email:
            user = db.session.query(User).filter_by(
                email=self.email.data).first()
            if user is not None:
                raise ValidationError('Sorry! Email already exists.')

     
       

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

class PhotoForm(FlaskForm):
    photo_one = FileField("Photo1", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'pdf'])])
    photo_two = FileField("Photo2", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'pdf'])])
    photo_three = FileField("Photo3", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'pdf'])])
    photo_one_name = StringField("Photo1 filename")
    photo_two_name = StringField("Photo2 filename")
    photo_three_name = StringField("Photo3 filename")
    submit = SubmitField("Submit")

class ContactGiverForm(FlaskForm):
    description = TextAreaField("Any message or inquiry goes here.", validators=[DataRequired()], render_kw={'rows':'10'})
    submit = SubmitField("Submit")

class ReplyForm(FlaskForm):
    description = TextAreaField('Reply message goes here.', validators=[DataRequired()], render_kw={'rows':'10'})
    submit = SubmitField("Reply")

class SearchForm(FlaskForm):
    query = StringField("Query", validators=[DataRequired()])
    submit = SubmitField('Submit')

class ContactAdminForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField("Message", validators=[DataRequired()], render_kw={'rows':'10'})
    submit = SubmitField("Contact")
