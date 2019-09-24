import socket
import json

class server:    
    def __init__(self):        
        with open('config.json') as json_file:
            data = json.load(json_file)
            ADDRESS = (data["HOST"],data["PORT"])
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(ADDRESS)
                s.listen()
                conn,addr = s.accept()
                print("Connected to {}".format(addr))
                serverClose = False
                with conn:     
                    while (not(serverClose)):                                                
                        data = conn.recv(1024)
                        data = data.decode()
                        isUserLoggedIn = True
                        while(isUserLoggedIn):
                            dataList = str(data).split('/')                            
                            if(int(dataList[0])==0):
                                self.userPanel(dataList[1],dataList[2],dataList[3])                                
                                message = "loggedout"
                                conn.sendall(message.encode()) 
                                isUserLoggedIn = False
                            else:
                                self.adminPanel(conn,dataList[1],dataList[2],dataList[3])
                                print("SUCESS")
                                isUserLoggedIn = False
                                serverClose = True

            s.close()

    def adminPanel(self, conn,username,fname,email):
        print("WELCOME TO ADMIN PANNEL")
        ch = 0 
        while(ch!=1):
            print("1.EXIT")
            ch = self.choiceValidation(1,2)
            if(ch == 1):
                message = "EXIT"
                conn.sendall(message.encode()) 
                       

    def userPanel(self,username,fname,email):
        ch = 0
        while(ch!=4):                
            print("WELCOME TO USER PANNEL")
            print("1. SEARCH BOOK CATALOGUE")
            print("2. BORROW")
            print("3. RETURN")
            print("4. LOGOUT")
            ch = self.choiceValidation(1,4)
            self.executeFuntion(ch,username,fname,email)

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
    
    def fnsearch(self,username,fname,email):
        print("SEARCH FUNCTION")        
    
    def fnborrow(self,username,fname,email):
        print("BORROW FUNCTION")
    
    def fnreturn(self,username,fname,email):
        print("RETURN FUNCTION")
    
    def fnlogout(self,username,fname,email):
        print("LOGOUT FUNCTION")

    _choice_and_function = {
            1 : fnsearch,
            2 : fnborrow,
            3 : fnreturn,
            4 : fnlogout
        }

    def executeFuntion(self,ch,username,fname,email):        
        func = self._choice_and_function.get(ch,lambda: 'Invalid Choice')
        return func(self,username,fname,email)                   

ser = server()