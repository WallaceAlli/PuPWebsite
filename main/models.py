from main import login_manager
from main.Sql import SQL_query
from main import mysql
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user_data = SQL_query.Load_Parent_User_id(mysql,int(user_id))
    if user_data:
        user = User(user_data['idGuardian'],user_data['guardianUsername'],user_data['guardianEmail'],user_data['guardianPassword'],user_data['guardianFirstName'],user_data['guardianLastName'])
        students = SQL_query.PrintStudent(mysql,user_data['idGuardian'])
        user.setParentData(user_data['guardianCar'],user_data['guardianDLNumber'],user_data['guardianLP'],user_data['guardianPhoneNumber'],students,user_data['guardianAddress'])
        user.setUsertype("Parent")
        

        with open('main\static\profile_pics\profile.jpg', 'wb') as file:
            file.write(user_data['guardianProfile_Pic'])
        
        with open('main\static\driver_license\driver-license.jpg','wb') as file:
            file.write(user_data['guardianDLPicture'])
        
        return user
    else:
        user_data = SQL_query.Load_Faculty_User_id(mysql,int(user_id))
        if user_data:
            user = User(user_data['idFaculty'],user_data['facultyUsername'],user_data['facultyEmail'],user_data['facultyPassword'],user_data['facultyFirstName'],user_data['facultyLastName'])
            user.setUsertype("Faculty")
            with open('profile.jpg', 'wb') as file:
                file.write(user_data['facultyPicture'])
            return user
    return None


class User(UserMixin):
    def __init__(self, ParentId,username,email,password,first_name,last_name):
        self.user_id = ParentId
        self.username = username
        self.email = email
        self.password = password
        self.image_file = 'profile.jpg'
        self.firstN = first_name
        self.LastN = last_name
        

    def setParentData(self,car,DLNum,LP,Phone,students,address):
        self.DLPic = 'driver-license.jpg'
        self.car = car
        self.DLNum = DLNum
        self.LP = LP
        self.phone = Phone
        self.students = students
        self.address = address

    def setUsertype(self,type):
        self.Usertype = type
    


    def setChild(self,children):
        self.children = children

    def get_id(self):
        return str(self.user_id)
    

    def is_active(self):
        return True
