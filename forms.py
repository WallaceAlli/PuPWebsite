from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(),Length(min =2 , max =20 )]) 
    # 'Username' will be the name/label in html 
    # Validators will be a list of guidelines we have for the username
    email = StringField('Email', validators= [DataRequired(), Email()])
    #The Datarequired() ensures that the user must input something into the Email Section
    # The Email() checks to make sure its a Email being entered
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    #Requires the Email to be Atleast 8 characters
    confirmpassword = PasswordField('ConfirmPassword', validators=[DataRequired(),Length(min=8), EqualTo('password')])
    # Requires the Confirm password section to be Equal to the Password Section
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


