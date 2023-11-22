from main import login_manager
from main.Sql import SQL_query
from main import mysql
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user_data = SQL_query.Load_Parent_User_id(mysql,int(user_id))
    if user_data:
        user = User(user_data['idGuardian'],user_data['guardianUsername'],user_data['guardianEmail'],user_data['guardianPassword'],user_data['guardianProfile_Pic'],user_data['guardianFirstName'],user_data['guardianLastName'])
        user.setParentData(user_data['guardianDLPicture'],user_data['guardianCar'],user_data['guardianDLNumber'],user_data['guardianLP'],user_data['guardianPhoneNumber'])
        user.setUsertype("Parent")
        return user
    else:
        user_data = SQL_query.Load_Faculty_User_id(mysql,int(user_id))
        if user_data:
            user = User(user_data['idFaculty'],user_data['facultyUsername'],user_data['facultyEmail'],user_data['facultyPassword'],user_data['facultyPicture'],user_data['facultyFirstName'],user_data['facultyLastName'])
            user.setUsertype("Faculty")
            return user
    return None

class User(UserMixin):
    def __init__(self, ParentId,username,email,password,profile_pic,first_name,last_name):
        self.user_id = ParentId
        self.username = username
        self.email = email
        self.password = password
        self.image_file = profile_pic
        self.firstN = first_name
        self.LastN = last_name
        

    def setParentData(self,picture,car,DLNum,LP,Phone):
        self.DLPic = picture
        self.car = car
        self.DLNum = DLNum
        self.LP = LP
        self.phone = Phone

    def setUsertype(self,type):
        self.Usertype = type
    


    def setChild(self,children):
        self.children = children

    def get_id(self):
        return str(self.user_id)
    

    def is_active(self):
        return True
