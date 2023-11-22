from datetime import datetime



class SQL_query:
    #This is the Query that will run if they selected that they are a Faculty allowing me to differntiate between
    # Parent and Teacher LogIns
    def Faculty_LogIn_query(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT idFaculty,facultyUsername,facultyEmail,facultyPassword,facultyPicture,facultyFirstName,facultyLastName FROM `faculty` WHERE facultyUsername = (%s)" 
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
        query = "SELECT idGuardian,guardianUsername,guardianEmail,guardianPassword, guardianProfile_Pic,guardianPhoneNumber,guardianFirstName,guardianLastName,guardianLP,guardianDLNumber,guardianDLPicture FROM `guardians` WHERE guardianUsername = (%s)" 
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
        mysql_cursor.execute(query,({form},User.user_id))
        # Do this when the things im using to query need to be different types
        # Picture file is a string and user_id is an int
        mysqlc.commit()
        mysql_cursor.close()
        mysqlc.close()

    def SingleQuery(mysql):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        mysql_cursor.execute("SELECT * FROM guardians")
        fetchdata = mysql_cursor.fetchall()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    
    def UpdateChat(mysql):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        mysql_cursor.execute("select facultyUsername,facultyPicture,messageContent,messagelogTime,messagelogDate,messagelogType from messagelog, faculty where idUser1 = idFaculty")
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


    
        
    



    

        

# For when I find a way to insert date into the Log, datetime.utcnow is what should be used