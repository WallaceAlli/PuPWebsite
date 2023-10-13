from flask import Flask, render_template
from forms import RegistrationForm,LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd8c3f8a28b8b162bbee3fca47e8e0b74'

@app.route("/")
def login():
    form = LoginForm()
    return render_template('login.html', title ='LogIn',form = form)
    #form = form gives us access to this form instance we just made in that template

def register():
    form = RegistrationForm()
    return render_template('register.html', title ='Register',form = form)
    #form = form gives us access to this form instance we just made in that template

if __name__ == '__main__':
    app.run(debug=True)