from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm


class UserLoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField()

class UserSignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[validators.DataRequired()])
    last_name = StringField("Last Name", validators=[validators.DataRequired()])
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField()