from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Email, EqualTo, Length

from app.auth.models import User

#Registration Form works
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid Email')])
    password = PasswordField('New Password',validators=[Length(min=8, max=80),
        InputRequired()])
    confirm = PasswordField('Repeat Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])
    submit = SubmitField("Register")
   
    # Custom email validation
    def validate_email(self, data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("An account with that email already exists")
 
 
#Login form works   
class LoginForm(FlaskForm): 
    username = StringField("Username", validators=[InputRequired(),  Length(min=3, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    


