__author__="Antigoni-k"
__description__="This is a replica of a login/sign-up panel connected to an SQL database. Please install the SQL CLI and necessary modules if you haven't already done so. To do this, use the following lines in your Command Prompt to install the required modules. Make sure Python is properly installed and added to the system's PATH, allowing you to install modules. SQL CLI: https://dev.mysql.com/downloads/mysql/ #pymysql: pip install pymysql #pillow: pip install pillow"


from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

window=Tk()
window.geometry("1000x500+200+100")
window.resizable(0,0)


canvas=Canvas(window, height=500, width=1000)

bg=ImageTk.PhotoImage(file='bgimage.jpg')
canvas.create_image(0, 0, anchor=NW, image=bg)


def login():

    def signupwindow():
        canvas.delete(loginformtext, usernametext, passwordtext)
        usernameentry.destroy()
        passwordentry.destroy()
        passwordshowbutton.destroy()
        signupformbutton.destroy()
        loginbutton.destroy()
        window.title("Signup Panel")

        def sushowpassword():
            su_password=str(su_passwordentry.get())
            if su_passwordentry.cget('show'):
                su_passwordentry.config(show="")
                su_passwordshowbutton.config(image=eyeiconcrossedout)
            else:
                su_passwordentry.config(show="●")
                su_passwordshowbutton.config(image=eyeicon)

        def showlogin():
            canvas.delete(signupformtext, nametext, suusernametext, su_passwordtext)
            nameentry.destroy()
            su_usernameentry.destroy()
            su_passwordentry.destroy()
            su_passwordshowbutton.destroy()
            loginformbutton.destroy()
            signupbutton.destroy()
            login()

        def signupuser():
            name=nameentry.get()
            username=su_usernameentry.get()
            password=su_passwordentry.get()
            if name!='' and username!='' and password!='':
                try:
                    databaseconnection=pymysql.connect(host='localhost', user='root', password='1234') #Please update any relevant information.
                    mycursor=databaseconnection.cursor()
                except:
                    error=messagebox.showwarning(title="Error", message="Check database connection and try again.")
                    return

                try:
                    query='CREATE DATABASE UserData'
                    mycursor.execute(query)
                    query='USE UserData'
                    mycursor.execute(query)
                    query='CREATE TABLE Users(Username varchar(30) primary key, Name varchar(30),  Password varchar(30))'
                    mycursor.execute(query)
                except:
                    mycursor.execute('USE UserData')
                capitalletters=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N" "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
                symbols=["!", "@", "#", "$", "%", "^", "&", "*"]
                capitallettercounter=0
                for capitalletter in capitalletters:
                    for x in password:
                        if capitalletter==x:
                            capitallettercounter+=1
                symbolscounter=0
                for symbol in symbols:
                    for x in password:
                        if symbol==x:
                            symbolscounter+=1
                if len(name)<1:
                    warning1=messagebox.showerror(title="Error", message="Please insert a name.")
                if len(username)<3:
                    warning2=messagebox.showerror(title="Error", message="The username should be at least 3 characters long.")
                mycursor.execute("SELECT Username FROM Users WHERE Username='%s'"%username)
                fetch_username=mycursor.fetchone()
                if fetch_username is not None:
                    warning3=messagebox.showerror(title="Error", message="This username is taken.")
                if capitallettercounter<2 or symbolscounter<1:
                    warning4=messagebox.showerror(title="Error", message="The password must contain at least two capital letters and one symbol.")
                x=0
                for symbol in symbols:
                    if username.find(symbol)==True:
                        warning5=messagebox.showerror(title="Error", message="Username cannot contain symbols.")
                        x+=1

                if len(username)>=3 and len(password)>=8 and capitallettercounter>=2 and symbolscounter>=1 and fetch_username==None and x==0:
                    query='INSERT INTO Users(Username, Name, Password) values(%s, %s, %s)'
                    mycursor.execute(query, (username, name, password))
                    databaseconnection.commit()
                    databaseconnection.close()
                    success=messagebox.showinfo(title="SignUp", message="User sign up was successful.")
                    showlogin()
            else:
                warning=messagebox.showerror(title="Error", message="Please fill out the form.")

        signupformtext=canvas.create_text(500, 140, text="SignUp Form", font="Corbel 28 bold", fill="white")
        nametext=canvas.create_text(350, 195, text="Name :", font="Corbel 15", fill="white")
        suusernametext=canvas.create_text(350, 225, text="Username :", font="Corbel 15", fill="white")
        su_passwordtext=canvas.create_text(350, 255, text="Password :", font="Corbel 15", fill="white")

        nameentry=Entry(window, width=27, font="Corbel 13")
        nameentry.place(x=450, y=185)

        su_usernameentry=Entry(window, width=27, font="Corbel 13")
        su_usernameentry.place(x=450, y=215)

        su_passwordentry=Entry(window, width=27, show="●", font="Corbel 13")
        su_passwordentry.place(x=450, y=245)

        eyeicon=ImageTk.PhotoImage(file='eyeicon.png')
        eyeiconcrossedout=ImageTk.PhotoImage(file='eyeiconcrossedout.png')
        su_passwordshowbutton=Button(window, command=sushowpassword, bd=0, image=eyeicon, width=21, height=21)
        su_passwordshowbutton.place(x=698, y=246)

        loginformbutton=Button(window, text="Have an account?", width=25, font="Corbel 10", command=showlogin)
        loginformbutton.place(x=310, y=310)

        signupbutton=Button(window, text="SignUp", font="Corbel 10", width=15, command=signupuser)
        signupbutton.place(x=570, y=310)
        
        


    def showpassword():
        password=str(passwordentry.get())
        if passwordentry.cget('show'):
            passwordentry.config(show="")
            passwordshowbutton.config(image=eyeiconcrossedout)
        else:
            passwordentry.config(show="●")
            passwordshowbutton.config(image=eyeicon)

    def loginuser():
        try:
            databaseconnection=pymysql.connect(host='localhost', user='root', password='1234') #please change information that apply
            mycursor=databaseconnection.cursor()
        except:
            error=messagebox.showwarning(title="Warning", message="Check database connection and try again.")
            return
        try:
            mycursor.execute("USE UserData")
            query=("SELECT Username FROM Users WHERE Username=%s")
            mycursor.execute(query, (usernameentry.get()))
            fetch_username=mycursor.fetchone()
            if fetch_username==None:
                loginfailure=messagebox.showerror(title="Error", message="User not found")
            else:
                query=("SELECT Password FROM Users WHERE Username=%s")
                mycursor.execute(query, (usernameentry.get()))
                fetch_password=mycursor.fetchone()
                password=str(passwordentry.get())
                if password==fetch_password[0]:
                    def close():
                        window.destroy()
                    canvas.delete(loginformtext)
                    canvas.delete(usernametext)
                    canvas.delete(passwordtext)
                    usernameentry.destroy()
                    passwordentry.destroy()
                    passwordshowbutton.destroy()
                    signupformbutton.destroy()
                    loginbutton.destroy()
                    loginsuccess=canvas.create_text(500, 210, text='Login successful!', fill="white", font="Corbel 30 bold")
                    okbutton=Button(window, text='OK!', font="Corbel 15", bd=0, width=20, command=close)
                    okbutton.place(x=385, y=270)
                else:
                    wrongpassword=messagebox.showerror(title="Error", message="Wrong password")
        except:
            warning=messagebox.showwarning(title='Warning', message='There is no user info yet. Be the first to sign up!')


    window.title("Login Panel")

    loginformtext=canvas.create_text(500, 150, text="Login Form", font="Corbel 28 bold", fill="white")
    usernametext=canvas.create_text(350, 215, text="Username :", font="Corbel 15", fill="white")
    passwordtext=canvas.create_text(350, 245, text="Password :", font="Corbel 15", fill="white") 

    usernameentry=Entry(window, width=27, font="Corbel 13", bd=0)
    usernameentry.place(x=450, y=205)
    

    passwordentry=Entry(window, width=27, show="●", font="Corbel 13", bd=0)
    passwordentry.place(x=450, y=235)

    eyeicon=ImageTk.PhotoImage(file='eyeicon.png')
    eyeiconcrossedout=ImageTk.PhotoImage(file='eyeiconcrossedout.png')
    passwordshowbutton=Button(window, command=showpassword, bd=0, image=eyeicon, width=21, height=21)
    passwordshowbutton.place(x=697, y=235)

    signupformbutton=Button(window, text="Don't have an account?", width=25, font="Corbel 10", command=signupwindow)
    signupformbutton.place(x=310, y=290)

    loginbutton=Button(window, text="Login", font="Corbel 10", width=15, command=loginuser)
    loginbutton.place(x=570, y=290)
    
    canvas.pack(side="left", fill="both", expand=True)


login()

window.mainloop()
