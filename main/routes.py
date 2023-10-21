from flask import render_template, url_for, flash, redirect, request
from main import app, bcrypt, mysql
# WHat ever I import/initialize in the init will have to be imported from main to other files if needed
from main.forms import RegistrationForm,LoginForm
from main.Sql import *
from main.models import User
from flask_login import login_user, current_user, logout_user,login_required
from main.models import User

@app.route("/home", methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = SQL_query.Parent_LogIn_query(mysql,form)
        if user_data and bcrypt.check_password_hash(user_data[3],form.password.data):
            user = User(user_data[0],user_data[1],user_data[2],user_data[3])
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
        flash(f'Account Created for {user}!', 'success')
        user_data = SQL_query.Register_query(mysql,form,hashed_pw)
        return redirect(url_for('profile'))
    return render_template('register.html', title ='Register',form = form)
    #form = form gives us access to this form instance we just made in that template

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))