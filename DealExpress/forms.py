from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from DealExpress.models import User

class SearchForm(FlaskForm):
    search_term = StringField("Search", validators=[DataRequired()])
    submit = SubmitField(label="Search")

class LoginForm(FlaskForm):
    username = StringField("UserName", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("UserName", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Sign up")
    
    """def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if User:
            raise ValidationError("username already taken!")
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if User:
            raise ValidationError("email already used!")"""