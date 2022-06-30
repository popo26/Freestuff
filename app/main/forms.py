from tokenize import String
from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length
from app.models import Category

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    bio = TextAreaField("Bio")
    submit = SubmitField("Submit")

class AdminLevelEditProfileForm(FlaskForm):
    username = StringField("Username", validators=[Length(0,64)])
    confirmed = BooleanField("Confirmed User?")
    role = SelectField("Role", coerce=int, choices=[(1, 'User'), (2, 'Administrator')]) #deal with it later
    name = StringField("Name", validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    bio = TextAreaField("Bio")
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    category = SelectField("Category", coerce=int, default=False, validators=[DataRequired()])
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

# class SearchForm(FlaskForm):
#     search = StringField("Search here", validators=[DataRequired()])
#     submit = SubmitField("Search", render_kw={'class': 'btn btn-success btn-block'})

class ContactGiverForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Any message or inquiry goes here.", validators=[DataRequired()], render_kw={'rows':'10'})
    submit = SubmitField("Submit")

