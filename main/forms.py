from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed,FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, FormField
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
    driver_license_num =  StringField('Driver License Number', validators= [DataRequired()]) 
    driver_license_pic = FileField('Upload Drivers License', validators=[Optional(),FileAllowed(['jpg','png'])])
    parentFName = StringField('First Name', validators= [DataRequired(),Length( max =30 )]) 
    parentLName = StringField('Last Name', validators= [DataRequired(),Length(max =30 )]) 
    PhoneNum = StringField('Phone Number', validators= [DataRequired(),Length(max =10 )]) 

    
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
    profile_pic = FileField('Update Profile Picture', validators=[Optional(),FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    driverlicense = StringField('Drivers License', validators=[Optional()])
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user =  SQL_query.check_username(mysql,username)
            if user :
                raise ValidationError('That User Name is taken. Please choose another username')



class PersonForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')

class MultiPersonForm(FlaskForm):
    people = FieldList(FormField(PersonForm), min_entries=1)

class AddKidsForm(FlaskForm):
    studentN = StringField('Student First Name', validators= [DataRequired()]) 
    studentL = StringField('Student Last Name', validators= [DataRequired()])
    grade = StringField('Student Grade Level', validators= [DataRequired()])
    submit = SubmitField('Add Student')



