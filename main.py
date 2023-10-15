from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm,LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd8c3f8a28b8b162bbee3fca47e8e0b74'

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'password':

        #This is where I will connect the code to the Database for the log in
            return redirect(url_for('profile')) 
        else:
            flash('Login Failed. Please Check your Login Information','danger')
    return render_template('login.html', title ='login',form = form)
    #form = form gives us access to this form instance we just made in that template

@app.route("/home")
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('profile'))
    return render_template('register.html', title ='Register',form = form)
    #form = form gives us access to this form instance we just made in that template

@app.route("/profile")
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)