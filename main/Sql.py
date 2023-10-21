from datetime import datetime

def load_user(user_id):
     return # the User ID from the Database

class SQL_query:
    def Faculty_LogIn_query(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT ParentId,username,password FROM `users` WHERE username = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        return user_data
    
    #Change this once tyler updates the SQL tables
    def Parent_LogIn_query(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT ParentId,username,email,password FROM `users` WHERE username = (%s)" 
        mysql_cursor.execute(query,({form.username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        return user_data
    #change the query to query from the Guardian Info Table
         
    def check_username(mysql,username):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT username FROM `users` WHERE username = (%s)" 
        mysql_cursor.execute(query,({username.data}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        return user_data
    
         
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
            return user_data
    
    def SingleQuery(mysql):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        mysql_cursor.execute("SELECT * FROM users")
        fetchdata = mysql_cursor.fetchone()
        mysql_cursor.close()
        return fetchdata
    
    def Load_user_id(mysql,form):
        mysqlc = mysql.connect
        mysql_cursor = mysqlc.cursor()
        query = "SELECT ParentId,username,email,password FROM `users` WHERE ParentId = (%s)" 
        mysql_cursor.execute(query,({form}))
        user_data = mysql_cursor.fetchone()
        mysql_cursor.close()
        return user_data
        
    
         
    
        
# For when I find a way to insert date into the Log, datetime.utcnow is what should be used