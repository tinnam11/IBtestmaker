# import mysql.connector
# from tkinter import messagebox
# from mysql.connector import Error
#
# try:
#     db = mysql.connector.connect(host="192.168.64.3", user="22TinnaM", password="test", database="test")
#     # you must create a Cursor object. It will let you execute all the queries you need
#     cur = db.cursor()
#     dbInfo = db.get_server_info()
#     print(dbInfo)
#     dbConn = cur.fetchone()
#     db.close()
#     print("success")
#     messagebox.showinfo("Database connection", "SUCCESS!  Connected to MySQL Server " + dbInfo)
# except Error as e:
#     messagebox.showinfo("Database connection failed")
#     print("error", e)

# # mycursor = mydb.cursor()

import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.64.3",
  user="22TinnaM	",
  password="test",
  # port=3307,
  database="test"
)

print(mydb)
dbInfo = mydb.get_server_info()
print(dbInfo)

#
# mycursor.execute("SHOW TABLES")
#
# for x in mycursor:
#   print(x)