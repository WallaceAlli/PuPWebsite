from main import login_manager
from main.Sql import SQL_query
from main import mysql
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user_data = SQL_query.Load_Parent_User_id(mysql,int(user_id))
    if user_data:
        user = User(user_data['parentId'],user_data['username'],user_data['email'],user_data['password'],user_data['profile_pic'])
        user.setUsertype("Parent")
        return user
    else:
        user_data = SQL_query.Load_Faculty_User_id(mysql,int(user_id))
        if user_data:
            user = User(user_data['idfaculty'],user_data['username'],user_data['email'],user_data['password'],user_data['profile_pic'])
            user.setUsertype("Faculty")
            return user
    return None

class User(UserMixin):
    def __init__(self, ParentId,username,email,password,profile_pic):
        self.user_id = ParentId
        self.username = username
        self.email = email
        self.password = password
        self.image_file = profile_pic

    def setUsertype(self,Usertype):
        self.Usertype = Usertype

    def setSchoolId(self,schoolId):
        self.schoolId = schoolId

    def setChild(self,children):
        self.children = children

    def get_id(self):
        return str(self.user_id)
    

    def is_active(self):
        return True
