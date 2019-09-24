import hashlib
import socket
import json
import time
from validate_email import validate_email
from databaseConnection import databaseConnection
from registerface import registerface
from recogniseface import recognise


class client:    
    d_c = databaseConnection()
    def __init__(self):                 
        with open('config.json') as json_file:
            data = json.load(json_file)
            ADDRESS = (data["HOST"],data["PORT"])        
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:            
                print("Connecting to {}...".format(ADDRESS))
                s.connect(ADDRESS)
                print("Connected")
                print("")
                print("########### WELCOME TO LIBRARY MANAGEMENT SYSTEM ###########") 
                userLogedIn = False
                while(not(userLogedIn)):
                    print("")
                    print("1.LOGIN      2.REGISTER")    
                    print("ENTER YOUR CHOICE?")
                    choice = self.choiceValidation(1,2)
                    if(choice==1):
                        valid,admin,u_n,fname,email = self.login()
                        if(valid):
                            if(admin==1):
                                print("WELCOME ADMIN")
                                message = str(admin)+"/"+str(u_n)+"/"+str(fname)+"/"+str(email)
                                s.send(message.encode())                                  
                                message = s.recv(1024)
                                message = message.decode()
                                if(message == "EXIT"):
                                    userLogedIn = True                                                            
                            else:
                                print("WELCOME USER")
                                message = str(admin)+"/"+str(u_n)+"/"+str(fname)+"/"+str(email)                                                            
                                s.send(message.encode())
                                message = s.recv(1024) 
                                message = message.decode()
                                print(message)   
                                print(userLogedIn)                       
                        else:
                            if(admin!=2):
                                print("INCORRECT PASSWORD")                                            
                    else:
                        self.register()        
                
                s.close()
    
    def login(self):
        recf = recognise()        
        username = recf.recogniseface()        
        if(username =="" or username==None):
            u_n = self.mandatoryInput("USERNAME: ",0)
            u_p = self.mandatoryInput("PASSWORD: ",2)
            hashedPassword = self.hashPassword(u_p)
            connect = self.d_c.getConnection()
            storedPassword = None
            adminFlag = 0
            with connect:
                itr = connect.cursor()
                itr.execute("SELECT pass,admin_flag,fname,email FROM user_details WHERE user_name = ?",(u_n,))            
                row = itr.fetchone()
                if(row!=None):
                    storedPassword = row[0]
                    adminFlag = row[1]
                    f_name = row[2]
                    email = row[3]
                else:
                    print("USERNAME DOES NOT EXIST!")
                    return(False,2,None,None,None)                     
            if(hashedPassword == storedPassword):
                return(True,adminFlag,u_n,f_name,email)
            else:
                return(False,adminFlag,u_n,None,None)
        else:
            u_n = username
            connect = self.d_c.getConnection()
            with connect:
                itr = connect.cursor()
                itr.execute("SELECT pass,admin_flag,fname,email FROM user_details WHERE user_name = ?",(u_n,))            
                row = itr.fetchone()
                if(row!=None):
                    storedPassword = row[0]
                    adminFlag = row[1]
                    f_name = row[2]
                    email = row[3]
                else:                    
                    return(False,2,None,None,None)
            return(True,adminFlag,u_n,f_name,email)

    def register(self):        
        firstname = self.mandatoryInput("FIRST NAME: ",0)                
        lastname = input("LAST NAME: ")
        email = self.mandatoryInput("EMAIL: ",1)
        username = self.mandatoryInput("USERNAME: ",0)
        match = False
        while(not(match)):
            password = self.mandatoryInput("PASSWORD: ",2)
            repeatPassword = self.mandatoryInput("RE-ENTER PASSWORD: ",2)
            if(password  == repeatPassword):
                match = True                      
                connect = self.d_c.getConnection()
                with connect:
                    itr = connect.cursor()                    
                    itr.execute("INSERT INTO user_details(user_name,pass,fname,lname,email,admin_flag) values ((?),(?),(?),(?),(?),(?))",(username,self.hashPassword(password),firstname,lastname,email,0))
                    print("REGISTRATION SUCESSFULL!")
            else:
                print("PASSWORDS DID NOT MATCH")
                match = False                            

    def choiceValidation(self,minVar,maxVar):
        ch = 0
        while(ch < minVar or ch > maxVar):
            try:
                ch = int(input())
            except:
                print("Invalid Input!. Please retry")
                ch = int(input("ENTER YOUR CHOICE?"))
            if(ch < minVar or ch > maxVar):
                print("Invalid Input!. Please retry")
                print("ENTER YOUR CHOICE?")
        return ch
    
    def hashPassword(self,password):
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        return password

    def mandatoryInput(self,text,type):
        inp = None
        while(inp == None or inp == ""):
            inp = input(text)
            if(type == 1 and inp != None and inp!=""):
                if(not(validate_email(inp))):
                    inp = None
            if(type == 2 and inp != None and inp!=""):
                if(len(inp)<8):
                    print("PASSWORD MUST BE ATLEAST 8 CHARACTERS")
                    inp = None
            if(type == 3 and inp != None and inp!="" and inp!="Y" and inp!="N"):
                print("PLEASE ENTER Y/N")
                inp = None
        return inp
        
c = client()