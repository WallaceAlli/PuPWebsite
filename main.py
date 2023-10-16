from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm,LoginForm
from flask_mysqldb import MySQL
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd8c3f8a28b8b162bbee3fca47e8e0b74'
app.config['MYSQL_HOST'] = '127.0.0.1' #Change this to Tylers IP address of his SQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ideapad320@'
app.config['MYSQL_DB'] = 'capstone'

mysql = MySQL()
mysql.init_app(app)


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT username, email, password FROM users WHERE username = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        global user_data 
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()

        if user_data is not None and form.email.data == user_data[1]:
            if form.password.data == user_data[2]:
                return redirect(url_for('profile'))
            else:
                flash(f'Wrong Password','danger')
        else:
            flash(f'No User Found or Wrong Email!','danger')
    return render_template('login.html', title ='login',form = form)
    #form = form gives us access to this form instance we just made in that template

@app.route("/home")
@app.route("/")
def home():
    mysqlc = mysql.connect
    mysql_cursor = mysqlc.cursor()
    mysql_cursor.execute("SELECT * FROM users")
    fetchdata = mysql_cursor.fetchone()
    mysql_cursor.close()
    return render_template('home.html', data = fetchdata)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO users (username, email, password,schooI) VALUES (%s, %s,%s,%s)"
        mysql_cursor.execute(query,({form.username.data},{form.email.data},{form.password.data},{form.SchoolID.data}))
        #mysql_cursor.execute("INSERT INTO users(`username`, `email`, `password`, `schooI') VALUES({form.username.data},{form.email.data},{form.password.data},{form.form.SchoolID.data})")
        mysqlc.commit()
        mysql_cursor.close()
        return redirect(url_for('profile'))
    return render_template('register.html', title ='Register',form = form)
    #form = form gives us access to this form instance we just made in that template

@app.route("/profile")
def profile():
    fetchdata = user_data
    return render_template('profile.html',data = fetchdata)

if __name__ == '__main__':
    app.run(debug=True)