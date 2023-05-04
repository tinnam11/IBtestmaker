import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import messagebox
import mysql.connector
from functools import partial


style = ttk.Style()
root = style.master
# style.configure('TLabel', font=('Helvetica', 20))

# #title + size of login window
root.title("Login Page")
root.geometry('1305x780')
root.resizable=(False,False)



global usernameEntry
global passwordEntry

#login page label
loginlb=ttk.Label(root,text='Login Page', font=('', 40))
loginlb.pack(anchor='center', pady=10)


#username text and input box
usernameLabel = ttk.Label(root, text="User Name:",font='Opensans 30')
usernameLabel.place(x=350, y=200)
username = tk.StringVar()
usernameEntry =ttk.Entry(root, font='Opensans 20', textvariable=username)
usernameEntry.place(x=600, y=200, height=40)

#password text and input box
passwordLabel = ttk.Label(root, text="Password:",font='Opensans 30')
passwordLabel.place(x=350, y=300)
password = tk.StringVar()
passwordEntry = ttk.Entry(root, font='Opensans 20', textvariable=password)
passwordEntry.place(x=600, y=300, height=40)

def deleteuserpass():
    print("Test delete")
    #usernameEntry.delete(0, 'end)
    #passwordEntry.delete(0, 'end')
    usernameEntry.set("test delete")


#hide password check button
var1=tk.IntVar()
def hidepass():
    if var1.get() == 1:
        passwordEntry =ttk.Entry(root, textvariable=password, show='*',font='Opensans 20',
                              bg='#EFF0F1').place(x=600, y=300, height=40)
    else:
        passwordEntry = ttk.Entry(root, textvariable=password, font='Opensans 20')\
            .place(x=600, y=300, height=40)
hidepassbutton=ttk.Checkbutton(root,text="hide pass", onvalue=1, variable=var1,
                           command=hidepass).place(x=760,y=350)

#validating password, checking if it matches databse
def validateLogin(username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root	",
        password="",
        # port=3307,
        database="test"
    )
    mycursor = mydb.cursor()
    username.get()
    password.get()
    #finding values from the specific user table
    sql = "select * from userprofile where User_ID = %s and Password = %s"
    mycursor.execute(sql,[(username.get()),(password.get())])
    results = mycursor.fetchall()
    #ssucessful, then transfer to homepage
    if results:
        for i in results:
            messagebox.showinfo("Error", "Successfully logged in")
            root.destroy()
            import homepage
            break
    #if wrong user pass, clear entry field
    else:
        messagebox.showinfo("Error", "Incorrect password. Please try again")
        deleteuserpass()

#login button + passing value
validateLogin= partial(validateLogin, username, password)
loginbutton=ttk.Button(root,text="Login",command=validateLogin,
                   width=12).place(x=713,y=400)




root.mainloop()

