from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length

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

