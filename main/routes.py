from flask import render_template, url_for, flash, redirect, request,jsonify,session,send_file
from flask_mail import Message
from main import app, bcrypt, mysql,mail
import qrcode #This is for the Qrcode that will be downloaded
import boto3
from io import BytesIO

# WHat ever I import/initialize in the init will have to be imported from main to other files if needed
from main.forms import RegistrationForm,LoginForm, UpdateAccountForm, AddKidsForm,EmailUser,VerifyCode, QrCodeGenerator,MultiPersonForm
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
    # ADD SQL STUFF
        # Process the form data, which is now a list of dictionaries
        return redirect(url_for('profile'))
    return render_template('AddKids.html', form=form)



@app.route("/profile", methods=['GET','POST'])
@login_required
def profile():
    if current_user.Usertype == "Parent":
        image_file = url_for('static',filename ='profile_pics/' + current_user.image_file )
        return render_template('parent_pages/profile.html',title='Profile',image_file= image_file)
    elif current_user.Usertype == "Faculty":
        image_file = url_for('static',filename ='profile_pics/' + current_user.image_file )
        return render_template('faculty_pages/faculty_profile.html',title ='Profile',image_file= image_file)

@app.route("/student-profile", methods=['GET','POST'])
def student_profile():
    return render_template('parent_pages/student_profile.html',title='Student Profile')

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
            picture_file = save_picture(form.profile_pic.data,'profile_pics')
            SQL_query.update_profile(mysql,form.profile_pic.name,picture_file,current_user)
        if form.username.data:
            SQL_query.update_profile(mysql,form.username.name,form.username.data,current_user)
        if form.email.data:
            SQL_query.update_profile(mysql,form.email.name,form.email.data,current_user)            
        return redirect(url_for('profile'))
    return render_template('parent_pages/update.html',title = 'updating', form = form)


def save_picture(form_picture,location):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/',location,picture_fn)
    form_picture.save(picture_path)
    return picture_fn
#END OF UPDATE THE PARENT PROFILE AND INFORMATION


@app.route("/queue", methods=['GET','POST'])
@app.route("/Queue", methods=['GET','POST'])
@login_required
def Queue():
    form = SQL_query.SingleQuery(mysql)
    return render_template("faculty_pages/queue.html",title='Queue',forms = form)

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
                user = User(user_data['idFaculty'],user_data['facultyUsername'],user_data['facultyEmail'],user_data['facultyPassword'],user_data['facultyPicture'],user_data['facultyFirstName'],user_data['facultyLastName'])
            else:
                user = User(user_data['idGuardian'],user_data['guardianUsername'],user_data['guardianEmail'],user_data['guardianPassword'],user_data['guardianProfile_Pic'],user_data['guardianFirstName'],user_data['guardianLastName'])
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


