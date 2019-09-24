import sqlite3 as sql_obj
import sys
import hashlib
dbname = 'local_database.db'
connect = sql_obj.connect(dbname)
with connect:
    itr = connect.cursor()
    itr.execute("DROP TABLE IF EXISTS user_details")        
    itr.execute("CREATE TABLE user_details(user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, user_name TEXT NOT NULL, pass TEXT NOT NULL, fname TEXT NOT NULL, lname TEXT, email TEXT NOT NULL, admin_flag INTEGER)")
    password = "hghar123"
    password = hashlib.md5(password.encode())
    password = password.hexdigest()
    itr.execute("INSERT INTO user_details(user_name,pass,fname,lname,email,admin_flag) values ((?),(?),(?),(?),(?),(?))",("jaqen",password,"Jack","quen","jack@gmail.com",1))
    connect.commit()