from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_term = StringField("Search", validators=[DataRequired()])
    submit = SubmitField(label="Search")

class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password1 = StringField("Enter Password", validators=[DataRequired()])
    password2 = StringField("Confirm Password", validators=[DataRequired()])
    #password 2 only in form, not models file, only need to check in form
    submit = SubmitField(label="Create Account")
