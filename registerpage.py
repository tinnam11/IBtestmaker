from tkinter import *
from tkinter import messagebox
from ttkbootstrap import Style
from functools import partial
import mysql.connector

style = Style()

#creating register page window
root=style.master
root.resizable=(False,False)
#default window size of window
root.geometry('1305x780')
#title of login window
root.title ('Register Page')
#register page text
top_title=Label( text="Register Page", font= 'Opensans 60', bg='#fcf1ef', fg='black')\
    .place(x=500, y=10)


#username text and input box
usernameLabel = Label(root, text="User Name:",font='Opensans 30').place(x=350, y=200)
username = StringVar()
usernameEntry = Entry(root, font='Opensans 20', textvariable=username, bg='#EFF0F1')\
    .place(x=600, y=200, height=40)

#password text and input box
passwordLabel = Label(root, text="Password:",font='Opensans 30').place(x=350, y=300)
password = StringVar()
passwordEntry = Entry(root, font='Opensans 20', textvariable=password, bg='#EFF0F1')\
    .place(x=600, y=300, height=40)

def registeruser():

    global username_info
    global password_info

    if len(username.get()) == 0 and len(password.get()) == 0:
        messagebox.showinfo("Error","Please fill in all required fields")

    if len(username.get()) == 0 and len(password.get()) != 0 :
            messagebox.showinfo("Error","Please enter Username")
    elif len(username.get()) != 0 and len(password.get()) == 0:
                    messagebox.showinfo("Error","Please enter Password")


    else:
        username_info = username.get()
        password_info = password.get()

        mydb = mysql.connector.connect(
            host="localhost",
            user="root	",
            password="",
            # port=3307,
            database="test"
        )
        mycursor = mydb.cursor()
        sqlFormula = "INSERT INTO userprofile (User_ID, Password) VALUES (%s, %s)"
        insertvar = (username_info, password_info)
        mycursor.execute(sqlFormula, insertvar)
        mydb.commit()

        username.set("")
        password.set("")
        messagebox.showinfo("Error", "Register succesfully")
        root.destroy()
        import loginpage

registerbutton=Button(root,text="Register",font='Opensans 20',command=registeruser, height=2,
                   width=12).place(x=713,y=400)

root.mainloop()