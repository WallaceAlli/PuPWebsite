from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_qrcode import QRcode

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd8c3f8a28b8b162bbee3fca47e8e0b74'
app.config['MYSQL_HOST'] = 'pickuppal.crnfzjphbive.us-east-2.rds.amazonaws.com' #Change this to Tylers IP address of his SQL
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'pickuppal'
app.config['MYSQL_DB'] = 'pupdatabase'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

#Mail Section
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Replace with your mail server port
app.config['MAIL_USE_TLS'] = True  # Set to False if your mail server doesn't support TLS
app.config['MAIL_USE_SSL'] = False  # Set to True if your mail server uses SSL
app.config['MAIL_USERNAME'] = 'kangutmus@gmail.com'  # Replace with your email address
app.config['MAIL_PASSWORD'] = 'ogko sphv aark wayf'  # Replace with your email password



mysql = MySQL()
mysql.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)
qrcode = QRcode(app)
#This is for the Qrcode that will be Shown on the HTML Page
login_manager.login_view = 'home'
login_manager.login_message_category = 'info'
from main import routes

