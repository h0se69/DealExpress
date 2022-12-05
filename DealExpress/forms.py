from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from DealExpress.models import User

#Search Form that recieves inputs from the user
class SearchForm(FlaskForm):
    search_term = StringField("Search", validators=[DataRequired()])
    submit = SubmitField(label="Search")

#Login Form that recieves inputs from the user
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

#SignUp Form that recieves inputs from the user
class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(message='Please choose a username.'), Length(min=3, max=20, message='Password must be between %(min)d and %(max)d characters.')])
    email = StringField("Email", validators=[DataRequired(message='Please enter an email.'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter a password.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='Please confirm password.'), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField(label="Sign up")
    #Helper function that makes sure username is availble
    '''def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if User:
            raise ValidationError("username already taken!")

    #Helper function that makes sure email is availble
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if User:
            raise ValidationError("email already used!")
            '''
class AccountDeleteForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField(label='Delete Account')

class ReactivateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField(label="Reactivate Account")