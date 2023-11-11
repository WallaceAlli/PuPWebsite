from flask import render_template, url_for, flash, redirect, request,jsonify
from main import app, bcrypt, mysql
# WHat ever I import/initialize in the init will have to be imported from main to other files if needed
from main.forms import RegistrationForm,LoginForm, UpdateAccountForm, AddKidsForm,MultiPersonForm
from main.Sql import *
from main.models import User
from flask_login import login_user, current_user, logout_user,login_required
from main.models import User
import secrets
import os


from datetime import datetime





@app.route("/Login", methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.Usertype == "Faculty":
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        if form.Usertype.data:
            user_data = SQL_query.Faculty_LogIn_query(mysql,form)

            if user_data and bcrypt.check_password_hash(user_data['password'],form.password.data):
                user = User(user_data['idfaculty'],user_data['username'],user_data['email'],user_data['password'],user_data['profile_pic'])
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f'LogIn Unsuccessful. Please check username or password','danger')
        else:
            user_data = SQL_query.Parent_LogIn_query(mysql,form)
            if user_data and bcrypt.check_password_hash(user_data['password'],form.password.data):
                user = User(user_data['parentId'],user_data['username'],user_data['email'],user_data['password'],user_data['profile_pic'])
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f'LogIn Unsuccessful. Please check username or password','danger')
    return render_template('login.html', title ='login',form = form)
    #The flash isnt working on the split screen so I cant send a error when they fail to log in
    # FIX THIS ITS VERY IMPORTANT AND SHOULD BE FIXED
    #form = form gives us access to this form instance we just made in that template

@app.route("/home")
@app.route("/")
def home():
    if  current_user.is_authenticated:
        form = LoginForm()
        return render_template('home.html', title='Home',form=form)
    else:
        return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        driver_pic = save_Driver_License(form.driver_license_pic.data)
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data = SQL_query.Register_query(mysql,form,hashed_pw,driver_pic)

        user = User(user_data['parentId'],user_data['username'],user_data['email'],user_data['password'],user_data['profile_pic'])
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))

    return render_template('register.html', title ='Register',form = form)
    #form = form gives us access to this form instance we just made in that template


@app.route("/add_more_info",methods=['GET','POST'])
def addKids():
    form = AddKidsForm()
    if form.validate_on_submit():
    # ADD SQL STUFF
        # Process the form data, which is now a list of dictionaries

        return redirect(url_for('profile'))
    return render_template('register_2.html', form=form)



@app.route("/add_more_info_2",methods=['GET','POST'])
def addKids_helper():
    return render_template('addkids_helper.html')













@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    if current_user.Usertype == "Parent":
        image_file = url_for('static',filename ='profile_pics/' + current_user.image_file )
        return render_template('parent_pages/profile.html',title='Profile',image_file= image_file)
    elif current_user.Usertype == "Faculty":
        image_file = url_for('static',filename ='profile_pics/' + current_user.image_file )
        return render_template('faculty_pages/faculty_profile.html',title ='Profile',image_file= image_file)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# Created for the Update App Route
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_Driver_License(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/driver_license',picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/update-parent-info", methods=['GET','POST'])
@login_required
def update():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data)
            SQL_query.update_profile(mysql,form.profile_pic.name,picture_file,current_user)
        if form.username.data:
            SQL_query.update_profile(mysql,form.username.name,form.username.data,current_user)
        if form.email.data:
            SQL_query.update_profile(mysql,form.email.name,form.email.data,current_user)            
        return redirect(url_for('profile'))
    return render_template('parent_pages/update.html',title = 'updating', form = form)


@app.route("/queue", methods=['GET','POST'])
@app.route("/Queue", methods=['GET','POST'])
@login_required
def Queue():
    form = SQL_query.SingleQuery(mysql)
    return render_template("faculty_pages/queue.html",title='Queue',forms = form)


@app.route("/request")
@app.route("/Request")
@login_required
def requestPickUp():
    return render_template("parent_pages/request.html",title='Request')

@app.route("/chat")
@app.route("/Chat")
@login_required
def chat():
    form= SQL_query.UpdateChat(mysql)
    return render_template("faculty_pages/chating.html",title='Chat',forms=form)

@app.route("/testing")
def testing():
    form = LoginForm()
    return render_template("testing.html",title='testing',form=form)

@app.route('/submit',methods=['GET','POST'])
@login_required
def submit():
    text = request.form['userInput']
    type = request.form['additionalValue']
    date_time = datetime.now()
    date = date_time.strftime("%Y-%m-%d")
    time = date_time.strftime("%I:%M %p")
    teacher_id = current_user.user_id
    SQL_query.Store_Chat(mysql,teacher_id,text,date,time,type)
    return f"Hello: {text}"

@app.route("/get_data",methods=['GET','POST'])
@login_required
def get_data():
    form = SQL_query.UpdateChat(mysql)
    return jsonify(form)



