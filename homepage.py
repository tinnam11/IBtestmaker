import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import *
import mysql.connector
from tkinter import messagebox

import addtest
import createalternateq
import createquestion
import databaseconnection
import editquestion


DB = databaseconnection.DBConnection()
import mytest
global plist
global checklist
import datetime
global questionresult

class Homepage:
    # contructor method for GUI - this contains the entire GUI for the hompage
    def __init__(self):
        #initialize style GUI
        self.s = Style()
        self.s.theme_use('lumen')
        self.s.configure('TNotebook.Tab', font=('', '15'))
        self.s.configure('primary.Treeview', rowheight=40)
        self.root = self.s.master
        self.root.title("Homepage")
        self.root.geometry('1400x780')

        #contructing the window,scrollbar
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill='both', expand=1)
        self.canvas = Canvas(self.mainframe)
        self.canvas.pack(side='left', fill='both', expand=1)
        self.scrollbar = ttk.Scrollbar(self.mainframe, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.secondframe = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.secondframe, anchor='nw')

        # #creating the tab control
        self.tabControl = ttk.Notebook(self.secondframe, width=1360, height=770)

        # creating all tabs including question, my test, and tags tab
        self.qtab = tk.Frame(self.secondframe)
        self.mttab = tk.Frame(self.secondframe)
        self.tagstab = tk.Frame(self.secondframe)

        # adding all of the tabs to main frame
        self.tabControl.add(self.qtab, text="Questions")
        self.tabControl.add(self.mttab, text="My Tests")
        self.tabControl.add(self.tagstab, text="Tags")

        #positioning the tabs frame
        self.qtab.grid_columnconfigure((0, 1), weight=1)
        self.qtab.grid_columnconfigure((0, 1), weight=1)
        self.mttab.grid_rowconfigure((0, 1), weight=1)
        self.mttab.grid_rowconfigure((0, 1), weight=1)
        self.tabControl.grid(row=0, column=0, sticky='nsew')

        # list of topics and subtopics later used to create the Checkbox Treeview
        #list
        self.topics = ['1:Stoichiometric Relationships', '2:Atomic Structure', '3:Periodicity',
                  '4:Chemical Bonding and Structure', '5:Energetics/Thermochemistry',
                  '6:Chemical Kinetics', '7:Equilibrium', '8:Acids and Bases', '9:Redox Processes',
                  '10:Organic Chemistry', '11: Measurement and Data Processing', '12:Atomic Structure (HL)',
                  '13:The Periodic Table (HL)', '14:Chemical Bonding and Structure (HL)',
                  '15:Energetics/Thermochemistry (HL)', '16:Chemical Kinetics (HL)', '17 Equilibrium (HL)',
                  '18:Acids and Bases (HL)', '19:Redox Processes (HL)', '20:Organic Chemistry (HL)',
                  '21:Measurement and Analysis (HL)']
        #2D list
        self.subtopic = [['1.1:Introduction to the particulate nature of matter and chemical change',
                     '1.2:The mole concept', '1.3: Reacting masses and volumes'], ['2.1:The nuclear atom',
                                                                                   '2.2:Electron configuration'],
                    ['3.1:Periodic table', '3.2:Periodic trends'],
                    ['4.1:Ionic bonding and structure', '4.2:Covalent bonding', '4.3:Covalent structures',
                     '4.4:Intermolecular forces', '4.5:Metallic bonding'], ['5.1:Measuring energy changes',
                                                                            '5.2:Hess’s Law', '5.3:Bond enthalpies'],
                    ['6.1:Collision theory and rates of reaction'],
                    ['7.1:Equilibrium'], ['8.1:Theories of acids and bases', '8.2:Properties of acids and bases',
                                          '8.3:The pH scale', '8.4:Strong and weak acids and bases',
                                          '8.5:Acid deposition'],
                    ['9.1:Oxidation and reduction', '9.2:Electrochemical cells'],
                    ['10.1:Fundamentals of organic chemistry',
                     '10.2:Functional group chemistry'], ['11.1:Uncertainties and errors in measurement and results',
                                                          '11.2:Graphical techniques',
                                                          '11.3:Spectroscopic identification of organic compounds'],
                    ['12.1:Electrons in atoms'], ['13.1:First-row d-block elements', '13.2:Coloured complexes'],
                    ['14.1:Covalent bonding and electron domain and molecular geometries', '14.2:Hybridization'],
                    ['15.1:Energy cycles', '15.2:Entropy and spontaneity'],
                    ['16.1:Rate expression and reaction mechanism',
                     '16.2:Activation energy'], ['17.1:The equilibrium law'], ['18.1:Lewis acids and bases',
                                                                               '18.2:Calculations involving acids and bases',
                                                                               '18.3:pH curves'],
                    ['19.1:Electrochemical cells'],
                    ['20.1:Types of organic reactions', '20.2:Synthetic routes', '20.3:Stereoisomerism'],
                    ['21.1:Spectroscopic identification of organic compounds']]

        #list of months and years to add to the tcombo box
        self.months = ('January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December')

        self.years = ('2008', '2009', '2010', '2011', '2012', '2013',
                 '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021')



        self.testname = DB.getTestnames()
        self.tagnames=DB.getTags()


        # declaring variable to store data from inputting fields
        self.selectttopic = tk.StringVar()
        self.searchqvar = tk.StringVar()
        self.sllevel = tk.IntVar()
        self.hllevel = tk.IntVar()
        self.p1style = tk.IntVar()
        self.p2style = tk.IntVar()
        self.selecttag1 = tk.StringVar()
        self.selecttag2 = tk.StringVar()
        self.selecttag3 = tk.StringVar()
        self.selectmonth = tk.StringVar()
        self.selectyear = tk.StringVar()
        self.test = tk.StringVar()

        # —————————— Question Tab —————————— #
        #creating all the filters input fields and commands such as tcombobox, text fileds,and button. Also positioning all of them in groups
        self.input_labelframe = ttk.Labelframe(self.qtab, text='Search questions', padding=(20, 20, 10, 5))
        self.input_labelframe.pack(side='top', fill='x', padx=10, pady=30)

        self.searchlb = ttk.Label(self.input_labelframe, text='Search')
        self.searchlb.grid(row=0, column=0, padx=3, sticky='ew')
        self.searchentrybox = ttk.Entry(self.input_labelframe, textvariable=self.searchqvar, width=40)
        self.searchentrybox.grid(row=0, column=1, padx=3, sticky='ew', columnspan=2)

        self.levelframe = ttk.Labelframe(self.input_labelframe, text='Level', padding=(20, 10, 10, 5))
        self.levelframe.grid(row=1, column=0, sticky='ew', columnspan=2, pady=10)
        self.slcb = ttk.Checkbutton(self.levelframe, text='SL', variable=self.sllevel, onvalue=1, offvalue=0,
                               style='secondary.TCheckbutton', command=self.levelcheck)
        self.slcb.grid(row=0, column=1, padx=3, pady=2, sticky='ew')
        self.hlcb = ttk.Checkbutton(self.levelframe, text='HL', variable=self.hllevel, onvalue=1, offvalue=0,
                               style='secondary.TCheckbutton', command=self.levelcheck)
        self.hlcb.grid(row=1, column=1, padx=3, pady=2, sticky='ew')

        self.paperframe = ttk.Labelframe(self.input_labelframe, text='Paper style', padding=(20, 10, 10, 5))
        self.paperframe.grid(row=1, column=2, sticky='ew', columnspan=2, pady=10, padx=10)
        self.p1cb = ttk.Checkbutton(self.paperframe, text='Paper 1', variable=self.p1style, onvalue=1, offvalue=0,
                               style='secondary.TCheckbutton')
        self.p1cb.grid(row=0, column=2, padx=3, pady=2, sticky='ew')
        self.p2cb = ttk.Checkbutton(self.paperframe, text='Paper 2', variable=self.p2style, onvalue=1, offvalue=0,
                               style='secondary.TCheckbutton')
        self.p2cb.grid(row=1, column=2, padx=3, pady=2, sticky='ew')

        self.tagframe = ttk.Labelframe(self.input_labelframe, text='Tags', padding=(20, 10, 10, 5))
        self.tagframe.grid(row=1, column=4, sticky='ew', columnspan=4, pady=10, padx=10)
        self.tog1box = ttk.Combobox(self.tagframe, textvariable=self.selecttag1, width=15)
        self.tog1box.grid(row=0, column=0, padx=3, pady=5, sticky='ew')
        self.tog1box['values'] = self.tagnames
        self.tog1box['state'] = 'readonly'
        self.tog1box.bind('<<ComboboxSelected>>', self.tag1check)
        self.tog2box = ttk.Combobox(self.tagframe, textvariable=self.selecttag2, width=15)
        self.tog2box.grid(row=0, column=1, padx=3, pady=5, sticky='ew')
        self.tog2box['values'] = self.tagnames
        self.tog2box['state'] = 'readonly'
        self.tog2box.bind('<<ComboboxSelected>>', self.tag2check)
        self.tog3box = ttk.Combobox(self.tagframe, textvariable=self.selecttag3, width=15)
        self.tog3box.grid(row=0, column=2, padx=3, pady=5, sticky='ew')
        self.tog3box['values'] = self.tagnames
        self.tog3box['state'] = 'readonly'
        self.tog3box.bind('<<ComboboxSelected>>', self.tag3check)
        self.edittagsbt = ttk.Button(self.tagframe, text='edit tags', style='warning.Outline.TButton', command=self.movetotagtab)
        self.edittagsbt.grid(row=0, column=3, padx=3, pady=5, sticky='ew')

        self.dateframe = ttk.Labelframe(self.input_labelframe, text='Exam Date', padding=(20, 10, 10, 5))
        self.dateframe.grid(row=1, column=9, sticky='ew', pady=10, padx=10, columnspan=4)
        self.monthbox = ttk.Combobox(self.dateframe, textvariable=self.selectmonth, width=20)
        self.monthbox.grid(row=0, column=1, sticky='ew', padx=3, pady=5)
        self.monthbox['values'] = self.months
        self.monthbox['state'] = 'readonly'
        self.monthbox.bind('<<ComboboxSelected>>', self.monthcheck)
        self.monthlb = ttk.Label(self.dateframe, text='Month')
        self.monthlb.grid(row=0, column=0)
        self.yearbox = ttk.Combobox(self.dateframe, textvariable=self.selectyear, width=20)
        self.yearbox.grid(row=0, column=3, sticky='ew', padx=3, pady=5)
        self.yearbox.bind('<<ComboboxSelected>>', self.yearcheck)
        self.yearlb = ttk.Label(self.dateframe, text='Year')
        self.yearlb.grid(row=0, column=2)
        self.yearbox['values'] = self.years
        self.yearbox['state'] = 'readonly'

        self.searchbt = ttk.Button(self.input_labelframe, text='Search questions', command=self.searchallq)
        self.searchbt.grid(row=2, column=5, sticky='nw', padx=10)
        self.resetbt = ttk.Button(self.input_labelframe, text='Reset filters', style='Outline.TButton', command=self.removeall)
        self.resetbt.grid(row=2, column=5, sticky='nw', padx=120)

        self.addqframe = ttk.Labelframe(self.input_labelframe, text='Add selected question to test', padding=(20, 10, 10, 10))
        self.addqframe.grid(row=3, column=5, columnspan=3, sticky='n', pady=10, padx=10)
        self.addtotestbt = ttk.Button(self.addqframe, text='Add selected questions', state='readonly')
        self.addtotestbt.grid(row=0, column=0, sticky='ew')
        self.qtotestlb = ttk.Label(self.addqframe, text='to the test')
        self.qtotestlb.grid(row=0, column=1, sticky='ew', padx=10)
        self.testbox = ttk.Combobox(self.addqframe, textvariable=self.test, width=30)
        self.testbox.grid(row=0, column=2, sticky='ew')
        self.testbox['values'] = self.testname
        self.testbox['state'] = 'readonly'
        self.addqbt = ttk.Button(self.addqframe, text='Add questions  +', style='success.TButton',
                            command=lambda: self.addqtotest(self.questionresult))
        self.addqbt.grid(row=0, column=8, sticky='ew', padx=10)

        self.editqframe = ttk.Labelframe(self.input_labelframe, text='Edit questions',padding=(20, 10, 10, 10))
        self.editqframe.grid(row=4, column=5, columnspan=3, sticky='n', pady=10, padx=10)
        self.createq=ttk.Button(self.editqframe,text='create new question', style='success.Outline.TButton', command=self.newq)
        self.createq.grid(row=0, column=0, sticky='ew', padx=10)
        self.editq = ttk.Button(self.editqframe, text='edit selected question', style='warning.Outline.TButton', command=self.edittheq)
        self.editq.grid(row=0, column=2, sticky='ew')
        self.createaddq = ttk.Button(self.editqframe, text='create alternate question', style='Outline.TButton', command=self.alternateq)
        self.createaddq.grid(row=0, column=3, sticky='ew', padx=10)

        #read all subtopics from the file and temporarily storing it in a list
        self.tempSubTopic = []
        with open('Chem_SubTopics.txt') as f:
            self.line = f.readlines()
            for self.lines in self.line:
                # remove newline or spacebar
                self.lines = self.lines.strip()
                self.tempSubTopic.append(self.lines)
                f.close()
        self.counter = 0
        self.arr_subtopic = []
        self.subtopic = []
        for i in range(0, len(self.tempSubTopic)):
            # assign number
            self.number_sub = self.tempSubTopic[i].split('.')
            self.number_topic = self.topics[self.counter].split(':')
            if (self.number_sub[0] == self.number_topic[0]):
                self.arr_subtopic.append(self.tempSubTopic[i])
            else:
                self.subtopic.append(self.arr_subtopic)
                self.arr_subtopic = []
                self.arr_subtopic.append(self.tempSubTopic[i])
                self.counter = self.counter + 1
                if (i == len(self.tempSubTopic) - 1):
                    self.subtopic.append(self.arr_subtopic)
        #creating key list and value list to organize the treeview
        self.checkbox = dict()
        for i in range(0, len(self.topics)):
            self.checkbox[self.topics[i]] = self.subtopic[i]
        self.key_list = list(self.checkbox.keys())
        self.value_list = list(self.checkbox.values())
        # contructing the treeview
        self.topiclb = ttk.Treeview(self.input_labelframe)
        self.topiclb.grid(row=2, column=0, columnspan=4, rowspan=10, sticky='ew')
        self.id = 22
        # Assign the various subtopics to each main topic (e.g. topic 1.4 goes under topic 1)
        for i in range(0, len(self.topics)):
            # Assign Topic
            self.topiclb.insert("", "end", i, text=self.key_list[i], values=(self.key_list[i],))
            #inserting the subtopic
            for j in range(0, len(self.value_list[i])):
                self.topiclb.insert(i, "end", self.id, text=self.value_list[i][j], values=(self.value_list[i][j],))
                self.id = self.id + 1

        # Contructing a question result treeview
        self.questionresult = ttk.Treeview(self.qtab, style='primary.Treeview', height=10)
        self.questionresult.pack(anchor='nw', fill='x', padx=10)
        self.questionresult['columns'] = ('Question', 'Total marks', 'Last used')
        self.questionresult.column('#0', width=0, stretch=NO)
        self.questionresult.column('Question', width=600, anchor='center')
        self.questionresult.column('Total marks', width=250, anchor='center')
        self.questionresult.column('Last used', width=200, anchor='center')
        self.questionresult.heading('#0', text='')
        self.questionresult.heading('Question', text='Question')
        self.questionresult.heading('Total marks', text='Total marks')
        self.questionresult.heading('Last used', text='Last used')

        #displaying results and organizing the tree with parents and children to make it easier to identify new alterations cerated from the question
        self.parentlist = DB.getparent()
        print(self.parentlist)
        self.id = len(self.parentlist)
        #looping to insert the parent into the treeview
        for i in range(0, len(self.parentlist)):
            self.questionresult.insert('', 'end', i, values=(
            self.parentlist[i][1], self.parentlist[i][11], self.parentlist[i][13],))
            self.childrenlist = DB.getchildren(str(self.parentlist[i][0]))
            #inserting children question into the subtreeview
            for j in range(0, len(self.childrenlist)):
                self.questionresult.insert(i, "end", self.id, values=(
                self.childrenlist[j][1], self.childrenlist[j][11], self.childrenlist[j][13],))
                self.id = self.id + 1

        #—————————— Test Tab —————————— #

        # initializing the varibales that would be stored to use in commands
        self.searchtestvar = tk.StringVar()
        self.selectfilter = tk.StringVar()

        #contructing the buttons, and tcombo box for seraching questions later on
        self.sortfilter = ('Most recently updated', 'A-Z', 'Z-A', 'Newest-Oldest', 'Oldest-Newest')

        self.mytest_labelframe = ttk.Labelframe(self.mttab, text='Search test', padding=(20, 10, 10, 5))
        self.mytest_labelframe.pack(side='top', fill='x', padx=10, pady=30)

        self.searchtestlb = ttk.Label(self.mytest_labelframe, text='Search')
        self.searchtestlb.grid(row=0, column=0, padx=3, sticky='ew')
        self.searchtestentrybox = ttk.Entry(self.mytest_labelframe, textvariable=self.searchtestvar, width=40)
        self.searchtestentrybox.grid(row=0, column=1, padx=3, sticky='ew', columnspan=2)

        self.sortbylb = ttk.Label(self.mytest_labelframe, text='Sort by')
        self.sortbylb.grid(row=0, column=5, padx=3, sticky='ew')
        self.sortbybox = ttk.Combobox(self.mytest_labelframe, textvariable=self.selectfilter, width=20)
        self.sortbybox.grid(row=0, column=6, sticky='ew', padx=3, pady=5)
        self.sortbybox['values'] = self.sortfilter
        self.sortbybox['state'] = 'readonly'

        self.searchtestbt = ttk.Button(self.mytest_labelframe, text='Search tests')
        self.searchtestbt.grid(row=0, column=7, sticky='ew', padx=15)
        self.addtestbt = ttk.Button(self.mytest_labelframe, text='Add new test +', command=self.addtest,
                               style='success.Outline.TButton')
        self.addtestbt.grid(row=0, column=8, sticky='ew', padx=8)
        self.deletetestbt = ttk.Button(self.mytest_labelframe, text='Delete test', command=self.deletetest,
                                  style='danger.Outline.TButton')
        self.deletetestbt.grid(row=0, column=9, sticky='ew', padx=8)

        self.testresultlb = ttk.Label(self.mttab, text='results:', font=('', '13'))
        self.testresultlb.pack(padx=10, pady=10, anchor='nw')

        # Constructing the treeview for displaying the test results
        self.testtreeview = ttk.Treeview(self.mttab, style='primary.Treeview', height=10)
        self.testtreeview.pack(fill='both', padx=10, pady=10)
        self.testtreeview['columns'] = ('testname', 'testdescription', 'lastused')
        self.testtreeview.column('#0', width=0, stretch=NO)
        self.testtreeview.column('testname', width=100, anchor='center')
        self.testtreeview.heading('#0', text='')
        self.testtreeview.heading('testname', text='Name')
        self.testtreeview.column('testdescription', width=150, anchor='center')
        self.testtreeview.heading('testdescription', text='Description')
        self.testtreeview.column('lastused', width=50, anchor='center')
        self.testtreeview.heading('lastused', text='Last Modified')
        self.alltest = DB.getAllTest()
        for j in range(len(self.alltest)):
            self.testtreeview.insert(parent='', index='end', iid=self.alltest[j][0], values=(self.alltest[j][1], self.alltest[j][2],self.alltest[j][5]))

        self.testtreeview.bind('<Double-1>', self.on_click)

        # —————————— Tags Tab —————————— #
        #contructing the input fields and the command buttons
        self.searchtagslb = ttk.Label(self.tagstab, text='Search')
        self.searchtagslb.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        self.searchtagsentry = ttk.Entry(self.tagstab, style='info.TEntry', width=30)
        self.searchtagsentry.grid(row=0, column=0, sticky='ew', padx=55, pady=10)
        self.searchtagsbt = ttk.Button(self.tagstab, text='Search', style='info.TButton')
        self.searchtagsbt.grid(row=0, column=1, sticky='nw', pady=10)

        self.tagsframe = ttk.Labelframe(self.tagstab, text='Edit tags', padding=(20, 20, 10, 10))
        self.tagsframe.grid(row=1, column=5, sticky='ew', padx=10, columnspan=10)
        self.nametaglb = ttk.Label(self.tagsframe, text='Tag')
        self.nametaglb.grid(row=0, column=0, sticky='ew', pady=5, padx=10)
        self.nametag = ttk.Entry(self.tagsframe)
        self.nametag.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        self.addtag = ttk.Button(self.tagsframe, text='add tag', command=self.addtag, style='success.TButton')
        self.addtag.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        self.deletetagbt = ttk.Button(self.tagsframe, text='delete selected tag', command=self.deletetag,
                                      style='danger.TButton')
        self.deletetagbt.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        self.edittagbt = ttk.Button(self.tagsframe, text='edit selected tag', command=self.edittag,
                                    style='warning.TButton')
        self.edittagbt.grid(row=1, column=2, sticky='ew', padx=10, pady=5)
        self.updatetagbt = ttk.Button(self.tagsframe, text='update tag', command=self.updatetag,
                                      style='primary.TButton')
        self.updatetagbt.grid(row=1, column=3, sticky='ew', padx=10, pady=5)

        self.alltagname = DB.getAllTag()

        # contsructing the treeview to display all the tags
        self.tagstreeview = ttk.Treeview(self.tagstab, style='primary.Treeview', height=10)
        self.tagstreeview.grid(row=1, column=0, sticky='ew', padx=10, columnspan=4, rowspan=20)
        self.tagstreeview['columns'] = ('Tagname')
        self.tagstreeview.column('#0', width=0, stretch=NO)
        self.tagstreeview.column('Tagname', width=150, anchor='center')
        self.tagstreeview.heading('#0', text='')
        self.tagstreeview.heading('Tagname', text='Tag Name')

        for i in range(len(self.alltagname)):
            self.tagstreeview.insert(parent='', index='end', iid=self.alltagname[i][0], values=(self.alltagname[i][1],))
        self.count = len(self.alltagname)

        self.root.mainloop()

        # searchalltest=tk.StringVar()

        # commands
        # navigate to tag tabs
    # function for the edit tag button that redirects to the tags tab
    def movetotagtab(self):
        self.tabControl.select(self.tagstab)

        # navigate to add question window
    # imports the add question window and pops up as a separate window
    def movetoaddq(self):
        self.root.destroy()
        import addquestion

        # input field
    # checks the month selected from the tcombo box and returns the value in a string - can be left as blank
    def monthcheck(self,event):
        x=self.selectmonth.get()
        print("month"+ x)
        return str(x)
    # checks the year selected from the tcombo box and returns the value in a string - can be left as blank
    def yearcheck(self, event):
        x=self.selectyear.get()
        print("year" + x)
        return str(x)
    def tag1check(self,event):
        x=self.selecttag1.get()
        return str(x)

    def tag2check(self, event):
        x = self.selecttag2.get()
        return str(x)
    def tag3check(self, event):
        x = self.selecttag3.get()
        return str(x)
    # uses the on value to check which checkbox for levels have been tickek and returns as string of selected level or null
    def levelcheck(self):
        if self.sllevel.get() == 1 and self.hllevel.get() == 1:
            return 'SL,HL'
        elif self.sllevel.get() == 0 and self.hllevel.get() == 1:
            return 'HL'
        elif self.hllevel.get() == 0 and self.sllevel.get() == 1:
            return 'SL'
        elif self.hllevel.get() == 0 and self.sllevel.get() == 0:
            return 'null'
    # checks the main topic that has been checked in the treeview and appended into a list
    def treeviewClick(self):  # Click
        self.list = []
        for self.item in self.topiclb.selection():
            self.item_text = self.topiclb.item(self.item, "values")
            self.list.append(self.item_text[0])
        return (self.list)  # Output the value of the first column of the selected row
    # checks the subtopic that has been selected and appends into the same list as the main topic
    def treeviewClicksub(self):  # Click
        self.list = []
        for self.item in self.topiclb.selection():
            self.item_text = self.topiclb.item(self.item, "values")
            self.list.append(self.item_text[0])
        return (self.list)  # Output the value of the first column of the selected row
    # uses the on value to check which checkbox for paper style have been tickek and returns as string of selected paper style or null
    def paperstylecheck(self):
        if self.p1style.get() == 1 and self.p2style.get() == 1:
            return 'Paper 1,Paper 2'
        elif self.p1style.get() == 0 and self.p2style.get() == 1:
            return 'Paper 2'
        elif self.p2style.get() == 0 and self.p1style.get() == 1:
            return 'Paper 1'
        elif self.p2style.get() == 0 and self.p1style.get() == 0:
            return 'null'


        # re updating the results everytime user presses search
    #function which resets the filters and removes all the question results
    def removeall(self):
        for self.record in self.questionresult.get_children():
            self.questionresult.delete(self.record)
    # function wich checks which checkbox or treeview has been clicked for the filter - this connects to the database and retrieves the correct result
    def searchallq(self):
        self.removeall()
        self.a = self.treeviewClick()
        self.b = self.levelcheck()
        self.c = self.paperstylecheck()
        self.d = self.treeviewClicksub()
        self.e = self.monthcheck('event')
        self.f = self.yearcheck('event')
        self.result = []
        if (len(DB.getLevel_paperstyle_topic_sub(self.b, self.a, self.d, self.c))) > 0:
            self.result = DB.getLevel_paperstyle_topic_sub(self.b, self.a, self.d, self.c)
        elif (len(DB.getLevel_paperstyle_topic(self.b, self.a, self.c))) > 0:
            self.result = DB.getLevel_paperstyle_topic(self.b, self.a, self.c)
        elif (len(DB.getPaperstyle_topic(self.a, self.c))) > 0:
            self.result = DB.getPaperstyle_topic(self.a, self.c)
        elif (len(DB.getPaperstyle_topic_sub(self.a, self.d, self.c)))>0:
            self.result = DB.getPaperstyle_topic_sub(self.a, self.d, self.c)
        elif (len(DB.getLevel_paperstyle_topic_sub_month_year(self.b, self.a, self.d, self.c, self.e, self.f))) > 0:
            self.result = DB.getLevel_paperstyle_topic_sub_month_year(self.b, self.a, self.d, self.c, self.e, self.f)
        for i in range(len(self.result)):
            self.questionresult.insert(parent='', index='end', iid=self.result[i][0],
                                      values=(self.result[i][1], self.result[i][11], self.result[i][13],))


        # --------- all functions within adding questions to a test
    #checks the questions that have been selected from the result and appends into a list
    def questionselect(self):  # Click
        global plist
        self.elist = []
        for self.item in self.questionresult.selection():
            self.item_text = self.questionresult.item(self.item, "values")
            self.elist.append(self.item_text[0])
        print(self.elist)

        self.tempstr = ""
        if len(self.elist) <= 0:
            self.tempstr = "'" + self.tempstr + "'"
        else:
            for i in range(len(self.elist)):
                if i == len(self.elist) - 1:
                    self.tempstr = self.tempstr + "'" + self.elist[i] + "'"
                else:
                    self.tempstr = self.tempstr + "'" + self.elist[i] + "',"
        print(self.tempstr)
        self.mydb = mysql.connector.connect(
                host="localhost",
                user="root	",
                password="",
                # port=3307,
                database="test"
            )
        self.mycursor = self.mydb.cursor()
        self.sql = "select No from newpastpaper where question in (" + self.tempstr + ")"
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.plist = []
        for i in self.results:
            self.plist.append(i[0])
        return (self.plist)
    #retrieves the existing questions in a test from the database and returns as a list
    def checkexistq(self):
        global checklist
        self.testname = self.test.get()
        self.mydb = mysql.connector.connect(
                host="localhost",
                user="root	",
                password="",
                # port=3307,
                database="test"
            )
        self.mycursor = self.mydb.cursor()
        self.sql = "select list_questionid from mytests where testname in ('" + self.testname + "')"
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        self.checklist = []
        for i in self.results:
            self.checklist.append(i[0])
        print(self.checklist)
        return (self.checklist)
    #adds new questions to the test by updating the question list column of selected test - also updates the date that question has been used
    def addqtotest(self,questionresult):
        self.plist = self.questionselect()
        self.checklist = self.checkexistq()
        self.testname = self.test.get()
        self.mydb = mysql.connector.connect(
                host="localhost",
                user="root	",
                password="",
                # port=3307,
                database="test"
            )
        self.temstr2 = str(self.checklist)
        print(self.temstr2)
        self.mycursor = self.mydb.cursor()
        self.tempstr = str(self.plist)

            # if questions already in string then add more questions, else append new string
        if self.temstr2 == "['']":
            self.list = self.tempstr[1:-1]
            print(self.list)
        else:
            self.listtem = self.temstr2[1:-2] + " ," + self.tempstr[1:-1]
            self.list = self.listtem[1:]
        print(self.list)

        self.sql = "update mytests set list_questionid= '" + self.list + "' where testname= '" + self.testname + "'"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.mydb.commit()
        for q in self.list:
            self.sql = "update newpastpaper set last_used= '" + str(datetime.date.today()) + "' where No= '" + q + "'"
            print(self.sql)
            self.mycursor.execute(self.sql)
            print("row " + str(self.mycursor.rowcount))
            self.mydb.commit()


        self.questionresult.delete(*self.questionresult.get_children())
        print('destoyed')
        self.result2 = []

        #add sleep time 
        if (len(DB.getAllquestion())) > 0:
            print("in")
            self.result2 = DB.getAllquestion()
            print(self.result2)
        for i in range(len(self.result2)):
            self.questionresult.insert(parent='', index='end', iid=self.result2[i][0], values=(
                self.result2[i][1], self.result2[i][11], self.result2[i][13],))
    # function to import the edit question page when a specific question is clicked on
    def edittheq(self):
        self.curItem = self.questionresult.focus()
        self.x=(self.questionresult.item(self.curItem,'values'))
        self.temp=(str(self.x[0]))
        self.temp2=(str(self.x[2]))
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root	",
            password="",
            # port=3307,
            database="test"
        )
        # creating a cursor to execute queries
        self.mycursor = self.mydb.cursor()
        self.sql="select * from newpastpaper where question = ('" + self.temp +"') and last_used = ('" + self.temp2 +"')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        # retrieve results from every row in database table
        self.results = self.mycursor.fetchone()
        self.k=(str(self.results[0]))
        self.A = editquestion.Editquestion(self.root, self.k)
    # function to import the alternate question page when a specific question is clicked on
    def alternateq(self):
        self.curItem = self.questionresult.focus()
        self.x = (self.questionresult.item(self.curItem, 'values'))
        self.temp = (str(self.x[0]))
        self.temp2 = (str(self.x[2]))
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root	",
            password="",
            # port=3307,
            database="test"
        )
        # creating a cursor to execute queries
        self.mycursor = self.mydb.cursor()
        self.sql = "select * from newpastpaper where question = ('" + self.temp + "') and last_used = ('" + self.temp2 + "')"
        print(self.sql)
        self.mycursor.execute(self.sql)
        # retrieve results from every row in database table
        self.results = self.mycursor.fetchone()
        self.k = (str(self.results[0]))
        self.A = createalternateq.Alternatequestion(self.root,self.k)
    # function to import the new question page when a specific question is clicked on
    def newq(self):
        self.A = createquestion.Newquestion(self.root)
     #----------------------------------------------test tab function
    # function to import the add test page when a specific question is clicked on
    def addtest(self):
        self.A = addtest.Newtest(self.root)
    # deletes the selected test from the treeview in the database table
    def deletetest(self):
        #identify the selected test from treeview
        self.x = self.testtreeview.selection()[0]
        #message box to confirm
        self.result = messagebox.askquestion("Delete test",
                                    "Are you sure you want to delete the test?",
                                    icon='warning')
        if self.result == 'yes':
            DB.deleteTest(self.x)
            self.testtreeview.delete(self.x)
       #if cancel then don't delete the test
        else:
            pass

        #determines which test have been clicked on in the treeview
    def on_click(self, event):
        self.x = self.testtreeview.selection()[0]
        self.A = mytest.MyTest(self.root,self.x)
    #-------------------------------------------tags tab function
    #add tags to the database
    def addtag(self):
        global count
        self.tagname = self.nametag.get()
        DB.addtag(self.tagname)
        self.tagstreeview.insert(parent='', index='end', iid=self.count, values=(self.tagname,))
        self.count += 1
        self.nametag.delete(0, 'end')
    #deletes the selected tag from the database
    def deletetag(self):
        self.x = self.tagstreeview.selection()[0]
        DB.deletetag(self.x)
        self.tagstreeview.delete(self.x)
    #edits the selected tag and update in the database
    def edittag(self):
        self.nametag.delete(0, 'end')
        self.selected = self.tagstreeview.focus()
        self.values = self.tagstreeview.item(self.selected, 'values')
        self.nametag.insert(0, self.values[0])
    # confirm to make changes to the edits
    def updatetag(self):
        self.tagname = self.nametag.get()
        self.selected = self.tagstreeview.focus()
        self.tagstreeview.item(self.selected, text='', values=(self.tagname,))
        DB.updatetag(self.selected, self.tagname)
Homepage()






