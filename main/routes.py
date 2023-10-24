from flask import render_template, url_for, flash, redirect, request
from main import app, bcrypt, mysql
# WHat ever I import/initialize in the init will have to be imported from main to other files if needed
from main.forms import RegistrationForm,LoginForm, UpdateAccountForm
from main.Sql import *
from main.models import User
from flask_login import login_user, current_user, logout_user,login_required
from main.models import User
import secrets
import os

@app.route("/home", methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        if current_user.Usertype == "Faculty":
            return redirect(url_for('faculty'))
        else:
            return redirect(url_for('profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.Usertype.data:
            user_data = SQL_query.Faculty_LogIn_query(mysql,form)
            if user_data and bcrypt.check_password_hash(user_data[3],form.password.data):
                user = User(user_data[0],user_data[1],user_data[2],user_data[3],user_data[4])
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f'{user}','danger')
                return redirect(next_page) if next_page else redirect(url_for('faculty'))
            else:
                flash(f'LogIn Unsuccessful. Please check username or password','danger')
        else:
            user_data = SQL_query.Parent_LogIn_query(mysql,form)
            if user_data and bcrypt.check_password_hash(user_data[3],form.password.data):
                user = User(user_data[0],user_data[1],user_data[2],user_data[3],user_data[4])
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f'{user}','danger')
                return redirect(next_page) if next_page else redirect(url_for('profile'))
            else:
                flash(f'LogIn Unsuccessful. Please check username or password','danger')
    return render_template('home.html', title ='login',form = form)
    #The flash isnt working on the split screen so I cant send a error when they fail to log in
    # FIX THIS ITS VERY IMPORTANT AND SHOULD BE FIXED
    #form = form gives us access to this form instance we just made in that template


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #hashes the password to encrypt it
        user = User(form.username.data,form.email.data,form.password.data)
        user_data = SQL_query.Register_query(mysql,form,hashed_pw)
        return redirect(url_for('profile'))
    return render_template('register.html', title ='Register',form = form)
    #form = form gives us access to this form instance we just made in that template





@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    if current_user.Usertype == "Parent":
        image_file = url_for('static',filename ='profile_pics/' + current_user.image_file )
        return render_template('parent_pages/profile.html',image_file= image_file)
    elif current_user.Usertype == "Faculty":
        return render_template('facultypage.html')



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Created for the Update App Route
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/update-parent-info", methods=['GET','POST'])
def update():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            SQL_query.update_profile_image(mysql,picture_file,current_user)
            if isinstance(picture_file,str):
                flash(f'{current_user.user_id}')
        return redirect(url_for('profile'))
    return render_template('parent_pages/update.html',title = 'updating', form = form)
