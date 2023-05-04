import tkinter as tk
import tkinter
from tkinter import ttk
from ttkbootstrap import Style
from ttkwidgets import CheckboxTreeview
from tkinter import *
import datetime
import mysql.connector
from tkinter import messagebox


class Edittest:
    def __init__(self,window,testid):
        self.style = Toplevel(window)
        self.root = self.style
        self.root.title("Edit test")
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
        self.testid=self.getfromtest(testid)
        self.tempstr = self.testid
        print(self.tempstr)
        #widgets
        self.ntlb=ttk.Label(self.root, text='New Test', font=('','40'))
        self.ntlb.grid(row=0, column=0, padx=20, pady=10, sticky='ew')

        self.namelb=ttk.Label(self.root, text='Name', font=('', '15'))
        self.namelb.grid(row=1, column=0, padx=20, pady=10, sticky='ew')
        self.tname=self.tempstr[1]
        self.nameentry=Text(self.root, width=100,height=2,font=("Helvetica", 16) )
        self.nameentry.grid(row=2, column=0, padx=20, pady=10, sticky='ew', columnspan=20)
        self.nameentry.insert(1.0,self.tname)

        self.descriptionlb=ttk.Label(self.root, text='Description', font=('','15'))
        self.descriptionlb.grid(row=3, column=0, padx=20, pady=10, sticky='ew')
        self.d=self.tempstr[2]
        self.descriptionbox=Text(self.root, width=100, height=15,font=("Helvetica", 16))
        self.descriptionbox.grid(row=4, column=0, padx=20, pady=10, sticky='ew',columnspan=20)
        self.descriptionbox.insert(1.0, self.d)

        self.createtestbt=ttk.Button(self.root, text='Create test', style='success.TButton', command=lambda:self.savetest(testid))
        self.createtestbt.grid(row=5, column=0, padx=20, pady=10, sticky='nw')
        self.orlb=ttk.Label(self.root, text='or')
        self.orlb.grid(row=5, column=0, padx=100, pady=15,sticky='nw')
        self.cancelbt=ttk.Button(self.root, text='Cancel', style='danger.Outline.TButton', command=self.canceltest)
        self.cancelbt.grid(row=5, column=0, padx=110)

        self.root.mainloop()



    def canceltest(self):
        self.root.destroy()
        import homepage

    def savetest(self,a):
        self.testname = self.nameentry.get("1.0", END)
        self.description = self.descriptionbox.get("1.0", END)
        self.sql = "UPDATE mytests SET testname = '" +self.testname+"', testdescription ='"+self.description+"' where testid = '"+a+"'"
        # SQL executing query
        self.mycursor.execute(self.sql)
        self.mydb.commit()
        # message box to show that question is added
        self.message = messagebox.showinfo('', 'successfully created a updated test!')
        self.root.destroy()
    def getfromtest(self,tid):
        # seraching for all columns with quesion id as key
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root	",
            password="",
            # port=3307,
            database="test"
        )
        # creating a cursor to execute queries
        self.mycursor = self.mydb.cursor()
        self.sql = "select * from mytests where testid = '" + tid + "'"
        # executing the search
        self.mycursor.execute(self.sql)
        # only obtain value from specific row
        self.results = self.mycursor.fetchone()
        # return the row
        return self.results
        print(self.results)