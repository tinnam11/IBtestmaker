import tkinter as tk
import tkinter
from tkinter import ttk
from ttkbootstrap import Style
from ttkwidgets import CheckboxTreeview
from tkinter import *
import datetime
import mysql.connector
from tkinter import messagebox


class Newtest:
    def __init__(self,window):
        self.style = Toplevel(window)
        self.root = self.style
        self.root.title("Add test")
        self.root.geometry('1400x780')

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root	",
            password="",
            # port=3307,
            database="test"
        )
        # creating a cursor to execute queries
        self.mycursor = self.mydb.cursor()

        #widgets
        self.ntlb=ttk.Label(self.root, text='New Test', font=('','40'))
        self.ntlb.grid(row=0, column=0, padx=20, pady=10, sticky='ew')

        self.namelb = ttk.Label(self.root, text='Name', font=('', '15'))
        self.namelb.grid(row=1, column=0, padx=20, pady=10, sticky='ew')
        self.nameentry = Text(self.root, width=100, height=2, font=("Helvetica", 16))
        self.nameentry.grid(row=2, column=0, padx=20, pady=10, sticky='ew', columnspan=20)

        self.descriptionlb = ttk.Label(self.root, text='Description', font=('', '15'))
        self.descriptionlb.grid(row=3, column=0, padx=20, pady=10, sticky='ew')
        self.descriptionbox = Text(self.root, width=100, height=15, font=("Helvetica", 16))
        self.descriptionbox.grid(row=4, column=0, padx=20, pady=10, sticky='ew', columnspan=20)


        self.createtestbt=ttk.Button(self.root, text='Create test', style='success.TButton', command=self.savetest)
        self.createtestbt.grid(row=5, column=0, padx=20, pady=10, sticky='nw')
        self.orlb=ttk.Label(self.root, text='or')
        self.orlb.grid(row=5, column=0, padx=100, pady=15,sticky='nw')
        self.cancelbt=ttk.Button(self.root, text='Cancel', style='danger.Outline.TButton', command=self.canceltest)
        self.cancelbt.grid(row=5, column=0, padx=110)

        self.root.mainloop()
    def canceltest(self):
        self.root.destroy()
        import homepage
    def savetest(self):
        self.testname = self.nameentry.get("1.0", END)
        self.description = self.descriptionbox.get("1.0",END)
        self.tempstr=""
        self.sql = "INSERT INTO mytests (testname, testdescription,lastused) VALUES (%s, %s, %s)"
        self.insertvar=(self.testname, self.description, str(datetime.date.today()))
        # SQL executing query
        self.mycursor.execute(self.sql, self.insertvar)
        self.mydb.commit()
        # message box to show that question is added
        self.message = messagebox.showinfo('', 'successfully created a new test!')
        self.root.destroy()
