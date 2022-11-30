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
    username = StringField("UserName", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

#SignUp Form that recieves inputs from the user
class SignupForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    username = StringField("UserName", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Sign up")
    #Helper function that makes sure username is availble
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if User:
            raise ValidationError("username already taken!")

    #Helper function that makes sure email is availble
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if User:
            raise ValidationError("email already used!")
