from main import login_manager
from main.Sql import SQL_query
from main import mysql
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user_data = SQL_query.Load_user_id(mysql,int(user_id))
    if user_data:
        user = User(user_data[0],user_data[1],user_data[2],user_data[3])
        return user
    return None

class User(UserMixin):
    def __init__(self, ParentId,username,email,password):
        self.user_id = ParentId
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.user_id)
    
    def is_active(self):
        return True

