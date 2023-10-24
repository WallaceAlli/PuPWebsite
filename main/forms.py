from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError, Optional
from main import mysql
from main.Sql import *


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(),Length(min =2 , max =20 )]) 
    # 'Username' will be the name/label in html 
    # Validators will be a list of guidelines we have for the username
    email = StringField('Email', validators= [DataRequired(), Email()])
    #The Datarequired() ensures that the user must input something into the Email Section
    # The Email() checks to make sure its a Email being entered
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    #Requires the Email to be Atleast 8 characters
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),Length(min=8), EqualTo('password')])
    # Requires the Confirm password section to be Equal to the Password Section
    submit = SubmitField('Sign Up')
    SchoolID = StringField('School ID', validators=[DataRequired()])
    
    def validate_username(self,username):
        user =  SQL_query.check_username(mysql,username)
        if user :
            raise ValidationError('That User Name is taken. Please choose another username')

class LoginForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(),Length(min =2 , max =20 )]) 
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    remember = BooleanField('Remember Me')
    Usertype = BooleanField('If Staff')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators= [Optional(),Length(min =2 , max =20 )]) 
    # 'Username' will be the name/label in html 
    # Validators will be a list of guidelines we have for the username
    email = StringField('Email', validators= [Optional(), Email()])
    picture = FileField('Update Profile Picture', validators=[Optional(),FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    driverlicense = StringField('Drivers License', validators=[Optional()])
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user =  SQL_query.check_username(mysql,username)
            if user :
                raise ValidationError('That User Name is taken. Please choose another username')


