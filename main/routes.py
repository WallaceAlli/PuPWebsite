from flask import render_template, url_for, flash, redirect, request,jsonify,session,send_file
from flask_mail import Message
from main import app, bcrypt, mysql,mail, socketio,emit
import qrcode #This is for the Qrcode that will be downloaded
from io import BytesIO

import base64

# WHat ever I import/initialize in the init will have to be imported from main to other files if needed
from main.forms import RegistrationForm,LoginForm, UpdateAccountForm, AddKidsForm,EmailUser,VerifyCode, QrCodeGenerator,MultiPersonForm,PickUpList
from main.Sql import *
from main.models import User
from flask_login import login_user, current_user, logout_user,login_required
from main.models import User
import secrets
import random
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
            if user_data and bcrypt.check_password_hash(user_data['facultyPassword'],form.password.data):
                session['user_type'] = form.Usertype.data
                session['user'] = user_data
                session['remember'] = form.remember.data
                return redirect(url_for('send_verification_code'))
            else:
                flash(f'LogIn Unsuccessful. Please check username or password','danger')
        else:
            user_data = SQL_query.Parent_LogIn_query(mysql,form)
            if user_data and bcrypt.check_password_hash(user_data['guardianPassword'],form.password.data):
                session['user_type'] = None
                session['user'] = user_data
                session['remember'] = form.remember.data
                return redirect(url_for('send_verification_code'))
        
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
        driver_pic = save_picture(form.driver_license_pic.data,'driver_license')
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data = SQL_query.Register_query(mysql,form,hashed_pw,driver_pic)
        user = User(user_data['idGuardian'],user_data['guardianUsername'],user_data['guardianEmail'],user_data['guardianPassword'],user_data['guardianProfile_Pic'],user_data['guardianFirstName'],user_data['guardianLastName'])

        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('profile'))

    return render_template('register.html', title ='Register',form = form)
    #form = form gives us access to this form instance we just made in that template


@app.route("/add-student-info",methods=['GET','POST'])
@login_required
def addKids():
    form = AddKidsForm()
    if form.validate_on_submit():
        SQL_query.InsertStudent(mysql,form.studentN.data,form.studentL.data,form.grade.data,form.address.data)
        student_id = SQL_query.StudentView(mysql,form.studentN.data)
        SQL_query.InsertView(mysql,current_user.user_id,student_id['idStudent'])

        return redirect(url_for('profile'))
    return render_template('AddKids.html', form=form)



@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    if current_user.Usertype == "Parent":
        image_file = url_for('static',filename ='profile_pics/profile.jpg' )
        
        return render_template('parent_pages/profile.html',title='Profile',image_file= image_file)
    elif current_user.Usertype == "Faculty":
        image_file = url_for('static',filename ='profile_pics/profile.jpg' )
        return render_template('faculty_pages/faculty_profile.html',title ='Profile',image_file= image_file)

@app.route("/student/<student_id>", methods=['GET','POST'])
def student_profile(student_id):
    student_info = SQL_query.grabstudentinfo(mysql,student_id)
    pickupinfo= SQL_query.grabList(mysql,student_id)
    white = pickupinfo[0]
    black = pickupinfo[1]
    return render_template('parent_pages/student_profile.html',title='Student Profile',form = student_info,white = white,black=black)

@app.route("/add-to-list/<student_id>",methods=['GET','POST'])
def AddList(student_id):
    form = PickUpList()
    if form.validate_on_submit():
        SQL_query.pickuplist(mysql,student_id,form)
        return redirect(url_for('profile'))
    return render_template('parent_pages/addlist.html',title='White or Black List',form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

#UPDATE THE PARENT PROFILE AND INFORMATION
@app.route("/update-parent-info", methods=['GET','POST'])
@login_required
def update():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_pic.data:
            save_picture(form.profile_pic.data,'profile_pics')
            with open('main/static/profile_pics/profile.jpg','rb') as file:
                New_Pic = file.read()
            SQL_query.update_profile(mysql,"guardianProfile_Pic",New_Pic,current_user)
        if form.username.data:
            SQL_query.update_profile(mysql,'guardianUsername',form.username.data,current_user)
        if form.email.data:
            SQL_query.update_profile(mysql,'guardianEmail'.email.name,form.email.data,current_user)   
        if form.PhoneNum.data:
            SQL_query.update_profile(mysql,'guardianPhoneNumber',form.username.data,current_user)
        if form.LP.data:
            SQL_query.update_profile(mysql,'guardianLP',form.LP.data,current_user)
        if form.car.data:
            SQL_query.update_profile(mysql,'guardianCar',form.car.data,current_user)
        if form.driver_license_pic.data:
            save_picture(form.driver_license_pic.data,'driver_license')
            with open('main/static/driver_license/driver-license.jpg','rb') as file:
                New_Pic = file.read()
            SQL_query.update_profile(mysql,"guardianDLPicture",New_Pic,current_user)


        return redirect(url_for('profile'))
    return render_template('parent_pages/update.html',title = 'updating', form = form)


def save_picture(form_picture,location):
    _, f_ext = os.path.splitext(form_picture.filename)
    if location == 'profile_pics':
        picture_fn = 'profile.jpg'
    else:
        picture_fn = 'driver-license.jpg'
    picture_path = os.path.join(app.root_path, 'static/',location,picture_fn)
    form_picture.save(picture_path)
    return picture_fn
#END OF UPDATE THE PARENT PROFILE AND INFORMATION


#THE FUNCTION AND CODE FOR THE QR CODE CREATION AND REQUEST PAGE
@app.route("/request", methods=['GET','POST'])
@app.route("/Request", methods=['GET','POST'])
@login_required
def requestPickUp():
    #SQL GET STUDENTS ASSOCIATED
    students = ["Tommy","Brian"]
    session['students']  = students       
    
    return render_template("parent_pages/request.html",title='Request',students=students)

#This will do the code to generate the QR Code based on the students selected
@app.route("/Generate", methods=['GET','POST'])
def Generate():
    students = session.get('students')
    print(students)
    Num_Students = len(students)
    Case = [0 for i in range(Num_Students) ]
    for i in range(Num_Students):
        Case[i] = request.form.get(students[i])
        print( request.form.get(students[i]))
    file = qrcode.make(Case)    
    print(Case)
    session['qrcode']=Case
    
    return render_template("parent_pages/downloadqrcode.html",title='Download',form=Case)  

@app.route("/download", methods=['POST','GET'])
def download():
    Case = session.get('qrcode')
    print(Case)
    file = qrcode.make(Case)    

    buf = BytesIO()
    file.save(buf)
    buf.seek(0)
    return send_file(buf,mimetype='image/jpeg',as_attachment=True,download_name="Qrcode.png")




#Function and Route for the Teacher Routes
@app.route("/chat")
@app.route("/Chat")
@login_required
def chat():
    form= SQL_query.UpdateChat(mysql)
    return render_template("faculty_pages/chating.html",title='Chat',forms=form)

@app.route('/submit',methods=['GET','POST'])
@login_required
def submit():
    text = request.form['userInput']
    type = request.form['additionalValue']
    date_time = datetime.now()
    date = date_time.strftime("%Y-%m-%d")
    time = date_time.strftime("%I:%M %p")
    teacher_id = current_user.user_id
    if text:
        SQL_query.Store_Chat(mysql,teacher_id,text,date,time,type)
    return f"Hello: {text}"

@app.route("/get_data",methods=['GET','POST'])
@login_required
def get_data():
    form = SQL_query.UpdateChat(mysql)
    
    return jsonify(form)
#END OF Function and Route for the Teacher Routes




#FUNCTIONS AND ROUTES TO ACCOMPLISH TWO STEP VERIFICATION
@app.route('/send_verification_code', methods=['GET', 'POST'])
def send_verification_code():
    form = EmailUser()

    if form.validate_on_submit():
        verification_code = str(random.randint(100000, 999999))
        session['verification_code'] = verification_code
        send_email(verification_code,form.email.data)

        return redirect(url_for('verify_code'))

    return render_template('send_verification_code.html',form=form)

@app.route('/verify_code',methods=['GET', 'POST'])
def verify_code():
    form = VerifyCode()
    if form.validate_on_submit():

        if form.code.data == session['verification_code']:
            user_data = session.get('user')
            remem = session.get('remember')
            user_type = session.get('user_type')
            if user_type:
                user = User(user_data['idFaculty'],user_data['facultyUsername'],user_data['facultyEmail'],user_data['facultyPassword'],user_data['facultyFirstName'],user_data['facultyLastName'])
            else:
                user = User(user_data['idGuardian'],user_data['guardianUsername'],user_data['guardianEmail'],user_data['guardianPassword'],user_data['guardianFirstName'],user_data['guardianLastName'])
            login_user(user, remember=remem)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'WRONG CODE ENTERED!! TRY AGAIN')
    return render_template('verify_code.html',form=form)

def send_email(code,email):
    msg = Message('Two-Step Verification Code',sender='kangutmus@gmail.com',recipients=[email])
    #CHANGE THE RECIEPIENT TO THE FORM.EMAIL.DATA SO IT WONT SEND IT TO ME BUT IT WILL SEND IT THE THE PERSONS EMAIL
    msg.body = 'Your Verification code is: '+ code
    mail.send(msg)
    return None
# END OF FUNCTIONS AND ROUTES TO ACCOMPLISH TWO STEP VERIFICATION


@app.route("/queue", methods=['GET','POST'])
@app.route("/Queue", methods=['GET','POST'])
@login_required
def Queue():
    return render_template("faculty_pages/queue.html",title='Queue')

@app.route("/get_Greenqueue",methods=['GET','POST'])
@login_required
def get_Greenqueue():
    form = SQL_query.grabQueue(mysql,'Green')
    return jsonify(form)

@app.route("/get_Yellowqueue",methods=['GET','POST'])
@login_required
def get_Yellowqueue():
    form = SQL_query.grabQueue(mysql,'Yellow')
    return jsonify(form)
