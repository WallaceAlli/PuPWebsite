from datetime import datetime

class SQL_query:
    #This is the Query that will run if they selected that they are a Faculty allowing me to differntiate between
    # Parent and Teacher LogIns
    def Faculty_LogIn_query(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT idFaculty,facultyUsername,facultyEmail,facultyPassword,facultyFirstName,facultyLastName FROM `faculty` WHERE facultyUsername = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data

    #Change this once tyler updates the SQL tables
    
    #change the query to query from the Guardian Info Table
    
    def check_username(mysql,username):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT guardianUsername FROM `guardians` WHERE guardianUsername = (%s)" 
        mysql_cursor.execute(query,({username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    
        #This is the Query that will be used when creating the Parents Account within the System
        #Might have to change it to allow teachers to register but that doesnt matter rn
    def Register_query(mysql,form,hashed_pw,driver_pic):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO guardians (guardianFirstName, guardianLastname,guardianPhoneNumber,guardianLP,guardianCar,guardianUsername,guardianPassword,guardianDLNumber,guardianProfile_Pic,guardianDLPicture,guardianEmail) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        mysql_cursor.execute(query,({form.parentFName.data},{form.parentLName.data},{form.PhoneNum.data},{form.LP.data},{form.car.data},{form.username.data},{hashed_pw},{form.driver_license_num.data},{"default.jpg"},{driver_pic},{form.email.data}))
        mysqlc.commit()
        #Added
        query = "SELECT * FROM guardians WHERE guardianUsername = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    
    def Load_Parent_User_id(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT * FROM `guardians` WHERE idGuardian = (%s)"
        mysql_cursor.execute(query,({form}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    
    def Parent_LogIn_query(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT idGuardian,guardianUsername,guardianEmail,guardianPassword,guardianFirstName,guardianLastName FROM `guardians` WHERE guardianUsername = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    
    # This was done so I could implement the Login Manager Package
    # I needed to be able to work around not using SQL alchemy where it would implement the isactive for me
    # So I was basically forced to call the User twice
    def Load_Faculty_User_id(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT idFaculty,facultyUsername,facultyEmail,facultyPassword, facultyPicture,facultyFirstName,facultyLastName  FROM `faculty` WHERE idFaculty = (%s)" 
        mysql_cursor.execute(query,({form}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data

    
    def Update_Parent(mysql,form): 
        mysqlc = mysql.connect
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        mysqlc.close()
        #query = "UPDATE faculty set "
         #finish this whenever u decide to make a update shit
    
    def update_profile(mysql,col_name,form,User):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "UPDATE `guardians` SET {} = (%s) WHERE `idGuardian` =  (%s)".format(col_name)
        mysql_cursor.execute(query,(form,User.user_id))
        # Do this when the things im using to query need to be different types
        # Picture file is a string and user_id is an int
        mysqlc.commit()
        mysql_cursor.close()
        mysqlc.close()
    
    def UpdateChat(mysql):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        mysql_cursor.execute("select facultyUsername,messageContent,messagelogTime,messagelogDate,messagelogType from messagelog, faculty where idUser1 = idFaculty")
        fetchdata = mysql_cursor.fetchall()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    
    def Store_Chat(mysql,user_id,chat,date,time,type):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO messagelog (idUser1, messageContent,messagelogDate,messagelogTime,messagelogType) VALUES (%s,%s, %s,%s,%s)"
        mysql_cursor.execute(query,(user_id,{chat},{date},{time},{type}))
        mysqlc.commit()
        mysql_cursor.close()
        mysqlc.close()

    def InsertStudent(mysql,firstname,lastname,grade,address):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO `students` (`studentFirstName`, `studentLastName`, `studentGrade`,`studentAddress`) VALUES (%s, %s, %s,%s)"
        mysql_cursor.execute(query,({firstname},{lastname},grade,{address}))
        mysqlc.commit()
        mysql_cursor.close()

    def StudentView(mysql,student):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "select idStudent from students where studentFirstName = (%s)"
        mysql_cursor.execute(query,({student}))
        fetchdata = mysql_cursor.fetchone()
        mysql_cursor.close()
        return fetchdata
    
    def InsertView(mysql,parentId,studentId):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO  `guardian_student` (idGuardian,idStudent) Values(%s,%s)"
        mysql_cursor.execute(query,(parentId,studentId))
        mysqlc.commit()
        mysql_cursor.close()
        mysqlc.close()

    def PrintStudent(mysql,parentId):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "select idStudent,studentFirstName,studentLastName,studentGrade from Parent_Students_View where idGuardian = (%s)"
        mysql_cursor.execute(query,({parentId}))
        fetchdata = mysql_cursor.fetchall()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    
    def check_studentN(mysql,student):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "select studentFirstName from students where studentFirstName = (%s)"
        mysql_cursor.execute(query,({student.data}))
        fetchdata = mysql_cursor.fetchall()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    
    def grabstudentinfo(mysql,studentid):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "select * from students where idStudent = (%s)"
        mysql_cursor.execute(query,({studentid}))
        fetchdata = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    
    def related(mysql,studentid):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "select guardianFirstName,guardianLastname,guardianPhoneNumber from Parent_Students_View where idStudent = (%s)"
        mysql_cursor.execute(query,({studentid}))
        fetchdata = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    def pickuplist(mysql,studentid,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO  `pickup_list` (idStudent,FirstName,Lastname,Type) Values(%s,%s,%s,%s)"
        mysql_cursor.execute(query,(studentid,{form.FirstName.data},{form.LastName.data},{form.Type.data}))
        mysqlc.commit()
        mysql_cursor.close()
        mysqlc.close()

    def grabList(mysql,studentid):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "select FirstName,LastName from pickup_list where idStudent = (%s) and `type` = 'White'"
        mysql_cursor.execute(query,({studentid}))
        fetchwhite = mysql_cursor.fetchall()
        query = "select FirstName,LastName from pickup_list where idStudent = (%s) and `type` = 'Black' "
        mysql_cursor.execute(query,({studentid}))
        fetchblack = mysql_cursor.fetchall()
        mysql_cursor.close()
        mysqlc.close()
        return fetchwhite,fetchblack
    
    def grabQueue(mysql,Type):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "select * from queue where `type` = (%s)"
        mysql_cursor.execute(query,({Type}))
        fetchdata = mysql_cursor.fetchall()
        mysql_cursor.close()
        return fetchdata
    








        



    
        
    



    

        

# For when I find a way to insert date into the Log, datetime.utcnow is what should be used