from datetime import datetime



class SQL_query:
    #This is the Query that will run if they selected that they are a Faculty allowing me to differntiate between
    # Parent and Teacher LogIns
    def Faculty_LogIn_query(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT idfaculty,username,email,password,profile_pic FROM `faculty` WHERE username = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    
    #Change this once tyler updates the SQL tables
    def Parent_LogIn_query(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT parentId,username,email,password,profile_pic FROM `users` WHERE username = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    #change the query to query from the Guardian Info Table
    
    def check_username(mysql,username):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT username FROM `users` WHERE username = (%s)" 
        mysql_cursor.execute(query,({username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    
        #This is the Query that will be used when creating the Parents Account within the System
        #Might have to change it to allow teachers to register but that doesnt matter rn
    def Register_query(mysql,form,hashed_pw):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO users (username, email, password,schoolId) VALUES (%s, %s,%s,%s)"
        mysql_cursor.execute(query,({form.username.data},{form.email.data},{hashed_pw},{form.SchoolID.data}))
        mysqlc.commit()
        #Added
        query = "SELECT username, email, password FROM users WHERE username = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        mysqlc.close()
        return user_data
    

    
    def Load_Parent_User_id(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT parentId,username,email,password, profile_pic FROM `users` WHERE ParentId = (%s)" 
        mysql_cursor.execute(query,({form}))
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
        query = "SELECT idfaculty,username,email,password, profile_pic  FROM `faculty` WHERE idfaculty = (%s)" 
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
        query = "UPDATE `users` SET {} = (%s) WHERE `ParentId` =  (%s)".format(col_name)
        mysql_cursor.execute(query,({form},User.user_id))
        # Do this when the things im using to query need to be different types
        # Picture file is a string and user_id is an int
        mysqlc.commit()
        mysql_cursor.close()
        mysqlc.close()

    def SingleQuery(mysql):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        mysql_cursor.execute("SELECT * FROM users")
        fetchdata = mysql_cursor.fetchall()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    
    def UpdateChat(mysql):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        mysql_cursor.execute("select username,profile_pic,chat from teacher_chat, faculty where teacher_id = idfaculty")
        fetchdata = mysql_cursor.fetchall()
        mysql_cursor.close()
        mysqlc.close()
        return fetchdata
    
    def Store_Chat(mysql,user_id,chat,time,chattype):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "INSERT INTO teacher_chat (teacher_id, chat,time,chat_type) VALUES (%s, %s,%s)"
        mysql_cursor.execute(query,(user_id,{chat},{time}))
        mysqlc.commit()
        mysql_cursor.close()
        mysqlc.close()


    
        
    



    

        

# For when I find a way to insert date into the Log, datetime.utcnow is what should be used