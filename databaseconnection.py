import mysql.connector
import codecs

class DBConnection:
    #contructor method to secure the connection with mySQL
    def __init__(self): #constructor
        #establishing connection of python with SQL
        self.mydb= mysql.connector.connect(
        host="localhost",
        user="root	",
        password="",
        # port=3307,
        database="test"
    )
        #creating a cursor to execute queries
        self.mycursor = self.mydb.cursor()
    #function to get all tags from database
    def getAllTag(self):
        self.list = []
        #query to select all tags from database table
        self.sql = "select * from tags"
        #execute the query
        self.mycursor.execute(self.sql)
        #fetch all rows from the database table
        self.results = self.mycursor.fetchall()
        for i in self.results:
            self.list.append(i)
        return self.list
    def gettagname(self):
        self.list=[]
        self.sql="select tagname from tags"
        self.mycursor.execute(self.sql)
        # fetch all rows from the database table
        self.results = self.mycursor.fetchall()
        for i in self.results:
            self.list.append(i)
        return (self.list)

    #query to add tags to the database table
    def addtag(self,tagname_info):
        self.sql = "insert into tags (tagname) VALUES ('" + tagname_info + "')"
        self.mycursor.execute(self.sql)
        self.mydb.commit()
    # query to delete tags to the database table
    def deletetag(self, tagid_info):
        self.sql = "delete from tags where tagid = '" + tagid_info + "'"
        self.mycursor.execute(self.sql)
        self.mydb.commit()
    # query to add update to the database table
    def updatetag(self, tagid_info, tagname_info):
        self.sql = "update tags set tagname = '" + tagname_info + "'  where tagid = '" + tagid_info + "'"
        self.mycursor.execute(self.sql)
        self.mydb.commit()
    # function to get all test from database
    def getAllTest(self):
        self.list = []
        self.sql = "select * from mytests"
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        for i in self.results:
            self.list.append(i)
        return self.list
    # query to delete test to the database table
    def deleteTest(self, testid_info):
        #delete test query
        self.sql = "delete from mytests where testid = '" + testid_info + "'"
        #executing the query
        self.mycursor.execute(self.sql)
        self.mydb.commit()
    def getTestnames(self):
        self.sql = "select * from mytests"
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        #loop in range of results
        for i in self.results:
            #add to the list
            self.list.append(i[1])
        return tuple(self.list)
    def getTags(self):
        self.sql = "select * from tags"
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i[1])
        return tuple(self.list)
    def getQuestionid(self, question):
        self.tempstr = ""
        if len(question) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(question)):
                if i == len(question) - 1:
                    self.tempstr = self.tempstr + "'" + question[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + question[i] + "',"
        self.sql="select questionid from newpastpaper where "+question+" in (" + self.tempstr + ")"
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i[0])
        print(self.list)
        return(self.list)
    # functions assigned in order for the client to use the filter search
        #this function gets all the questions as a preview
    def getAllquestion(self):

        self.sql = "select * from newpastpaper"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getparent(self):
        self.sql = "select * from newpastpaper where parent = 0"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getchildren(self, parentid):
        self.sql = "select * from newpastpaper where parent = '"+parentid+"'"

        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list

        # this function allows to search paper level, topic, subtopic and paper style
    #all functions which works with the filter in the homepage GUI to search queries from the database - these combinations are ones that client will use - the result is appended in a list
    def getLevel_paperstyle_topic_sub(self, paperlevel,selecttopic, selectsubtopic, paperstyle):
        #creating empty strings
        self.tempstr = ""
        self.tempstr2=""
        if len(selecttopic) <= 0:
            #keep as empty string
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range (len(selecttopic)):
                if i == len(selecttopic)-1:
                    #insert the topic and end the string
                    self.tempstr = self.tempstr + "'" + selecttopic[i]+ "'"
                else:
                    #add comma add the end tp continue the string
                    self.tempstr = self.tempstr + "'" + selecttopic[i]+ "',"
        if len(selectsubtopic)<= 0:
            self.tempstr2="'"+self.tempstr2+"'"
        else:
            #loop through the subtopic list - add subtopic to the string
            for i in range (len(selectsubtopic)):
                if i == len(selectsubtopic)-1:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i]+ "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i]+ "',"

        #SQL search query
        self.sql="select * from newpastpaper where level in ('" + paperlevel +"') and topic in (" + self.tempstr + ") " \
                "and subtopic in (" + self.tempstr2 + ") and Exam_paper_style in ('" + paperstyle + "')"
       #executing the query
        self.mycursor.execute(self.sql)
        #retrieve results from every row in database table
        self.results=self.mycursor.fetchall()
        self.list=[]
        for i in self.results:
            self.list.append(i)
        return self.list
        # this function allows to search paper level, topic and paper style
    def getLevel_paperstyle_topic(self, paperlevel, selecttopic, paperstyle):
        self.tempstr = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        self.sql = "select * from newpastpaper where level in ('" + paperlevel + "') and topic in (" + self.tempstr + ") and Exam_paper_style in ('" + paperstyle + "')"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getPaperstyle_topic(self,selecttopic, paperstyle):
        self.tempstr = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range (len(selecttopic)):
                if i == len(selecttopic)-1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i]+ "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i]+ "',"

        self.sql="select * from newpastpaper where topic in (" + self.tempstr + ") and Exam_paper_style in ('" + paperstyle + "')"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results=self.mycursor.fetchall()
        self.list=[]
        for i in self.results:
            self.list.append(i)
        return self.list
    def getPaperstyle_topic_sub(self, selecttopic, selectsubtopic, paperstyle):
        self.tempstr = ""
        self.tempstr2 = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        if len(selectsubtopic) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(selectsubtopic)):
                if i == len(selectsubtopic) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "',"

        self.sql = "select * from newpastpaper where topic in (" + self.tempstr + ") and subtopic in (" + self.tempstr2 + ") and Exam_paper_style in ('" + paperstyle + "')"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getLevel_paperstyle_topic_sub_month_year(self, paperlevel, selecttopic, selectsubtopic, paperstyle, month, year):
        print(selecttopic)
        print(selectsubtopic)
        self.tempstr = ""
        self.tempstr2 = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        if len(selectsubtopic) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(selectsubtopic)):
                if i == len(selectsubtopic) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "',"


        self.sql = "select * from newpastpaper where level in ('" + paperlevel + "') and topic in (" + self.tempstr + ") and subtopic in (" + self.tempstr2 + ") and Exam_paper_style in ('" + paperstyle + "') and Exam_month in ('" + month + "') and Exam_year in ('" + year + "')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
        # this function allows to search paper level, topic and paper style
    def getPaperstyle_topic_sub_tag(self, selecttopic, selectsubtopic, paperstyle,tag):
        self.tempstr = ""
        self.tempstr2 = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        if len(selectsubtopic) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(selectsubtopic)):
                if i == len(selectsubtopic) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "',"

        self.sql = "select * from newpastpaper where topic in (" + self.tempstr + ") and subtopic in (" + self.tempstr2 + ") and Exam_paper_style in ('" + paperstyle + "') and tag in ('"+tag+"')"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getPaperstyle_topic_tag(self, selecttopic, paperstyle,tag):
        self.tempstr = ""
        self.tempstr2 = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"

        self.sql = "select * from newpastpaper where topic in (" + self.tempstr + ") and Exam_paper_style in ('" + paperstyle + "') and tag in ('"+tag+"')"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getLevel_topic_sub_month_year(self, paperlevel, selecttopic, selectsubtopic, month,year):
        print(selecttopic)
        print(selectsubtopic)
        self.tempstr = ""
        self.tempstr2 = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        if len(selectsubtopic) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(selectsubtopic)):
                if i == len(selectsubtopic) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "',"

        self.sql = "select * from newpastpaper where level in ('" + paperlevel + "') and topic in (" + self.tempstr + ") and subtopic in (" + self.tempstr2 + ") and Exam_month in ('" + month + "') and Exam_year in ('" + year + "')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getmonth_year(self,month, year):
        print(month)
        print(month)
        self.tempstr = ""
        self.tempstr2 = ""
        if len(month) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(month)):
                if i == len(month) - 1:
                    self.tempstr = self.tempstr + "'" + month[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + month[i] + "',"
        if len(month) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(month)):
                if i == len(month) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + month[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + month[i] + "',"


        self.sql = "select * from newpastpaper where Exam_month in ('" + month + "') and Exam_year in ('" + year + "')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
        # this function allows to search paper level, topic and paper style
    def getmonth(self,month):
        print(month)
        print(month)
        self.tempstr = ""
        self.tempstr2 = ""
        if len(month) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(month)):
                if i == len(month) - 1:
                    self.tempstr = self.tempstr + "'" + month[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + month[i] + "',"
        if len(month) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(month)):
                if i == len(month) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + month[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + month[i] + "',"


        self.sql = "select * from newpastpaper where Exam_month in ('" + month + "')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def get_year(self,year):
        self.sql = "select * from newpastpaper where Exam_year in ('" + year + "')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def gettopic(self,selecttopic):
        self.tempstr = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        self.sql = "select * from newpastpaper where topic in (" + self.tempstr + ")"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def gettopic_sub(self, selecttopic, selectsubtopic):
        self.tempstr = ""
        self.tempstr2 = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        if len(selectsubtopic) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(selectsubtopic)):
                if i == len(selectsubtopic) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "',"

        self.sql = "select * from newpastpaper where topic in (" + self.tempstr + ") and subtopic in (" + self.tempstr2 + ")"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getLevel(self, paperlevel):
        self.tempstr = ""
        self.tempstr2=""
        if len(paperlevel) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range (len(paperlevel)):
                if i == len(paperlevel)-1:
                    self.tempstr = self.tempstr + "'" + paperlevel[i]+ "'"
                else:
                    self.tempstr = self.tempstr + "'" + paperlevel[i]+ "',"
        if len(paperlevel)<= 0:
            self.tempstr2="'"+self.tempstr2+"'"
        else:
            for i in range (len(paperlevel)):
                if i == len(paperlevel)-1:
                    self.tempstr2 = self.tempstr2 + "'" + paperlevel[i]+ "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + paperlevel[i]+ "',"

        self.sql="select * from newpastpaper where level in ('" + paperlevel +"')"
        # print(self.sql)
        self.mycursor.execute(self.sql)
        self.results=self.mycursor.fetchall()
        self.list=[]
        for i in self.results:
            self.list.append(i)
        return self.list
    def getmonth_year_tag(self, month,year,tag):
        self.sql = "select * from newpastpaper where Exam_month in ('" + month + "') and Exam_year in ('" + year + "') and tag in ('"+tag+"')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list
    def getLevel_paperstyle_topic_sub_month_year_tag(self, paperlevel, selecttopic, selectsubtopic, paperstyle, month, year,tag):
        print(selecttopic)
        print(selectsubtopic)
        self.tempstr = ""
        self.tempstr2 = ""
        if len(selecttopic) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(selecttopic)):
                if i == len(selecttopic) - 1:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + selecttopic[i] + "',"
        if len(selectsubtopic) <= 0:
            self.tempstr2 = "'" + self.tempstr2 + "'"
        else:
            for i in range(len(selectsubtopic)):
                if i == len(selectsubtopic) - 1:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "'"
                else:
                    self.tempstr2 = self.tempstr2 + "'" + selectsubtopic[i] + "',"


        self.sql = "select * from newpastpaper where level in ('" + paperlevel + "') and topic in (" + self.tempstr + ") and subtopic in (" + self.tempstr2 + ") and Exam_paper_style in ('" + paperstyle + "') and Exam_month in ('" + month + "') and Exam_year in ('" + year + "') and tag in ('" + tag + "')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.list = []
        for i in self.results:
            self.list.append(i)
        return self.list






