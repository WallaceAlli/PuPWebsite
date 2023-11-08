from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd8c3f8a28b8b162bbee3fca47e8e0b74'
app.config['MYSQL_HOST'] = '127.0.0.1' #Change this to Tylers IP address of his SQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ideapad320@'
app.config['MYSQL_DB'] = 'capstone'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"



mysql = MySQL()
mysql.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
login_manager.login_message_category = 'info'
from main import routes
