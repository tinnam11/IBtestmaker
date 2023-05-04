import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root	",
        password="",
        # port=3307,
        database="test"
    )
mycursor = mydb.cursor()
sql="select * from newpastpaper where No in (3,4)"
mycursor.execute(sql)
results = mycursor.fetchall()
ilist=[]
for i in results:
    ilist.append(i[4])
print(ilist)