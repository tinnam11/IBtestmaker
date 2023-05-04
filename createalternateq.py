from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk
from ttkbootstrap import Style
import mysql.connector
import tkinter as tk
from PIL import Image,ImageTk
import datetime
from tkinter import messagebox


global open_status_name
open_status_name = False
global selected
selected = False


class Alternatequestion:
    def __init__(self, window,question_id):
        self.style = Toplevel(window)
        self.root = self.style
        self.root.title("Alternate question")
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

        self.question_id = question_id

        # create main frame
        self.my_frame = Frame(self.root)
        self.my_frame.pack(pady=5)
        # -------------------------------- For questions text box
        # Questions label
        self.questionlabel = ttk.Label(self.my_frame, text='Alternate question', font=('', 30))
        self.questionlabel.pack(anchor=W, pady=5)
        # create tool bar frame
        self.toolbar_frame = ttk.Frame(self.my_frame)
        self.toolbar_frame.pack(pady=5, anchor=W)
        # answer space selection
        self.answerspaceframe = ttk.Labelframe(self.toolbar_frame, text='answer space')
        self.answerspaceframe.grid(row=0, column=3, padx=10)
        self.selected_month = tk.StringVar()
        self.answerlines = ('2 lines', '3 lines', '4 lines', '5 lines', '6 lines')
        self.answerspace = ttk.Combobox(self.answerspaceframe, textvariable=self.selected_month)
        self.answerspace['values'] = self.answerlines
        self.answerspace['state'] = 'readonly'  # normal
        self.answerspace.grid(row=0, column=3, padx=5)
        # Text format frame
        self.textframe = ttk.Labelframe(self.toolbar_frame, text='text format')
        self.textframe.grid(row=0, column=0, sticky='ew', padx=10)
        # special charcters
        self.specialchar = ttk.Labelframe(self.toolbar_frame, text='special characters')
        self.specialchar.grid(row=0, column=1, sticky='ew', padx=10)
        self.scbut = ttk.Button(self.specialchar, text='special characters', command=self.popup_bonus)
        self.scbut.grid(row=0, column=0, padx=5)
        self.textboxframe = ttk.Frame(self.my_frame)
        self.textboxframe.pack(fill=BOTH, pady=5)

        #creating a
        self.tempstr=self.getAllq(self.question_id)
        self.my_image = ""

        # create text box
        self.my_text = Text(self.textboxframe, width=80, height=4, font=("Helvetica", 16),
                       selectbackground="gray",
                       selectforeground="black", undo=True,
                       wrap="none")
        # insert text into textbox
        self.question = self.tempstr[1]
        self.my_text.insert(1.0, self.question)
        # create scrollbar for textbox
        self.text_scroll = ttk.Scrollbar(self.textboxframe, orient='vertical', command=self.my_text.yview)
        self.text_scroll.grid(row=0, column=5, sticky='ns')
        # yscrollcommand=text_scroll.set,
        self.my_text.grid(row=0, column=0, columnspan=4, pady=5)
        self.my_text.config(spacing1=10)  # Spacing above the first line in a block of text
        self.my_text.config(spacing2=10)  # Spacing between the lines in a block of text
        self.my_text.config(spacing3=10)  # Spacing after the last line in a block of text
        # configure scroll bar
        self.my_text['yscrollcommand'] = self.text_scroll.set
        # import image frame + button
        self.importimframe = ttk.Labelframe(self.toolbar_frame, text="import image")
        self.importimframe.grid(row=0, column=2, padx=10)
        self.imagebut = ttk.Button(self.importimframe, text="add image", command=self.add_image)
        self.imagebut.grid(row=0, column=0, padx=5)
        # create menu
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        # ----------------------------------------------- textbox for answer choice (paper 1 only)
        # answer choice label
        self.aswclabel = ttk.Label(self.my_frame, text='Answer Choice', font=('', 30))
        self.aswclabel.pack(anchor=W, pady=5)
        self.aswcframe = ttk.Frame(self.my_frame)
        self.aswcframe.pack(fill=BOTH, pady=5)
        # create text box
        self.my_text3 = Text(self.aswcframe, width=80, height=5, font=("Helvetica", 16),
                             selectbackground="yellow",
                             selectforeground="black", undo=True,
                             wrap="none")
        self.ascwchoice = self.tempstr[2]
        self.my_text3.insert(1.0, self.ascwchoice)
        # create scrollbar for textbox
        self.text_scroll3 = ttk.Scrollbar(self.aswcframe, orient='vertical', command=self.my_text3.yview)
        self.text_scroll3.grid(row=0, column=5, sticky='ns')
        # yscrollcommand=text_scroll.set,
        self.my_text3.grid(row=0, column=0, columnspan=4, pady=5)
        self.my_text3.config(spacing1=10)  # Spacing above the first line in a block of text
        self.my_text3.config(spacing2=10)  # Spacing between the lines in a block of text
        self.my_text3.config(spacing3=10)  # Spacing after the last line in a block of text
        # configure scroll bar
        self.my_text3['yscrollcommand'] = self.text_scroll3.set
        # ------------------------------- text box for marksheme
        # marksheme label
        self.marklabel = ttk.Label(self.my_frame, text='Markscheme', font=('', 30))
        self.marklabel.pack(anchor=W, pady=5)
        self.markschemeframe = ttk.Frame(self.my_frame)
        self.markschemeframe.pack(fill=BOTH, pady=5)
        # create text box
        self.my_text2 = Text(self.markschemeframe, width=80, height=5, font=("Helvetica", 16),
                        selectbackground="yellow",
                        selectforeground="black", undo=True,
                        wrap="none")
        self.marksceme = self.tempstr[3]
        self.my_text2.insert(1.0, self.marksceme)

        # create scrollbar for textbox
        self.text_scroll2 = ttk.Scrollbar(self.markschemeframe, orient='vertical', command=self.my_text2.yview)
        self.text_scroll2.grid(row=0, column=5, sticky='ns')
        # yscrollcommand=text_scroll.set,
        self.my_text2.grid(row=0, column=0, columnspan=4, pady=5)
        self.my_text2.config(spacing1=10)  # Spacing above the first line in a block of text
        self.my_text2.config(spacing2=10)  # Spacing between the lines in a block of text
        self.my_text2.config(spacing3=10)  # Spacing after the last line in a block of text
        # configure scroll bar
        self.my_text2['yscrollcommand'] = self.text_scroll2.set
        # --------------------------------------
        self.savebt = ttk.Button(self.my_frame, text='save', style='success.TButton', command=self.savequestion)
        self.savebt.pack(anchor=S, side=RIGHT)

        # self.homepagebt=ttk.Button(self.my_frame, text='back to homepage', style='TButton', command=self.backhome)
        # self.homepagebt.pack(anchor=S, side=LEFT)
        # add file menu
        self.file_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # add edit menu
        self.edit_menu = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=lambda: self.cut_text(False), accelerator="Command-X")
        self.edit_menu.add_command(label="Copy", command=lambda: self.copy_text(False), accelerator="Command-C")
        self.edit_menu.add_command(label="Paste", command=lambda: self.paste_text(False),
                              accelerator="Command-V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.my_text.edit_undo, accelerator="Command-Z")
        self.edit_menu.add_command(label="Redo", command=self.my_text.edit_redo, accelerator="Shift-Command-Z")

        # create status bar
        self.status_bar = Label(self.root, text="ready     ", anchor=E)
        self.status_bar.pack(fill=X, side=BOTTOM, ipady=5)

        # edit bindings
        self.root.bind('<Command-Key-x>', self.cut_text)
        self.root.bind('<Command-Key-c>', self.copy_text)
        self.root.bind('<Command-Key-y>', self.paste_text)

        # create buttons
        self.bold_button = ttk.Button(self.textframe, text="bold", command=self.bold_it)
        self.bold_button.grid(row=0, column=0, sticky='w', padx=5)
        self.italics_button = ttk.Button(self.textframe, text="italics", command=self.italics_it)
        self.italics_button.grid(row=0, column=1, sticky='w', padx=5)
        self.undo_button = ttk.Button(self.textframe, text="undo", command=self.my_text.edit_undo)
        self.undo_button.grid(row=0, column=2, sticky='w', padx=5)
        self.redo_button = ttk.Button(self.textframe, text="redo", command=self.my_text.edit_redo)
        self.redo_button.grid(row=0, column=3, sticky='w', padx=5)
        self.color_text_button = ttk.Button(self.textframe, text="Text color", command=self.text_color)
        self.color_text_button.grid(row=0, column=4, sticky='w', padx=5)

        self.root.mainloop()
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root	",
        password="",
        # port=3307,
        database="test"
    )
        self.mycursor = self.mydb.cursor()


# scrollbar = Scrollbar(root)
# scrollbar.pack(side=RIGHT, fill=Y)



#create new file function
    def new_file(self):
        #delete previous text
        self.my_text.delete("1.0", END)
        self.root.title('New file')
        self.status_bar.config(text="New file    ")
#open files
    def open_file(self):
        # delete previous text
        self.my_text.delete("1.0", END)
        self.root.title('New file')
        #grab filename
        self.text_file=filedialog.askopenfilename(initialdir=".", title="Open File", filetypes=(("Text Files","*.txt"),("HTML Files", "*.html"), ("Python Files","*.py"),("All Files", "*")))
        #check if filenname exist
        if self.text_file:
            global open_status_name
            self.open_status_name=self.text_file
        #update status bar
        self.name=self.text_file
        self.status_bar.config(text=self.name)
        self.name=self.name.replace("/Users/22TinnaM","")
        self.root.title(self.name)
        #open the file
        self.text_file=open(self.text_file, 'r')
        #add file to textbox
        self.stuff=self.text_file.read()
        self.my_text.insert(END,self.stuff)
        #close file
        self.text_file.close()


    #save as file
    def save_as_file(self):
        self.text_file=filedialog.asksaveasfilename(defaultextension=".*", initialdir=".", title="Open File", filetypes=(("Text Files","*.txt"),("HTML Files", "*.html"), ("Python Files","*.py"),("All Files", "*")))
        if self.text_file:
            #update status bar
            self.name=self.text_file
            self.status_bar.config(text="Saved:"+(self.name))
            self.root.title(self.name)
            #save the file
            self.text_file=open(self.text_file,'w')
            self.text_file.write(self.my_text.get(1.0,END))
            #close the file
            self.text_file.close()
    def save_file(self):
        global open_status_name
        if self.open_status_name:
            #save the file
            self.text_file=open(self.open_status_name,'w')
            self.text_file.write(self.my_text.get(1.0,END))
            #close the file
            self.text_file.close()
            self.status_bar.config(text="Saved:" + (self.open_status_name))
        else:
            self.save_as_file()
    #cut text function
    def cut_text(self,e):
        global selected
        if e:
            self.selected=self.root.clipboard_get()
        else:
            if self.my_text.selection_get():
                #grab selected text
                self.selected=self.my_text.selection_get()
                #delete text from text box
                self.my_text.delete("sel.first", "sel.last")
                # clear the clipboard then append
                self.root.clipboard_clear()
                self.root.clipboard_append(self.selected)

# copy text function
    def copy_text(self,e):
        global selected
        #check if use keyboard shortcut
        if e:
            self.selected=self.root.clipboard_get()
        if self.my_text.selection_get():
            # grab selected text
            self.selected = self.my_text.selection_get()
            #clear the clipboard then append
            self.root.clipboard_clear()
            self.root.clipboard_append(self.selected)


    # copy text function
    def paste_text(self,e):
        global selected
        if e:
            self.selected=self.root.clipboard_get()
        else:
            if self.selected:
                self.position=self.my_text.index(INSERT)
                self.my_text.insert(self.position, selected)

    #bold function
    def bold_it(self):
        #create font
        self.bold_font=font.Font(self.my_text, self.my_text.cget("font"))
        self.bold_font.configure(weight="bold")
        #configure a tag
        self.my_text.tag_configure("bold", font=self.bold_font)
        #define current tags
        self.current_tags=self.my_text.tag_names("sel.first")
        #if statement to see tag set
        if "bold" in self.current_tags:
            self.my_text.tag_remove("bold","sel.first", "sel.last")
        else:
            self.my_text.tag_add("bold", "sel.first", "sel.last")




    def italics_it(self):
        # create font
        self.italics_font = font.Font(self.my_text, self.my_text.cget("font"))
        self.italics_font.configure(slant="italic")
        # configure a tag
        self.my_text.tag_configure("italic", font=self.italics_font)
        # define current tags
        self.current_tags = self.my_text.tag_names("sel.first")
        # if statement to see tag set
        if "italic" in self.current_tags:
            self.my_text.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.my_text.tag_add("italic", "sel.first", "sel.last")

    def text_color(self):
        my_color=colorchooser.askcolor()[1]
        if self.my_color:
            self.status_bar.config(text=self.my_color)
            # create font
            self.color_font = font.Font(self.my_text, self.my_text.cget("font"))
            # configure a tag
            self.my_text.tag_configure("colored", font=self.color_font, foreground=self.my_color)
            # define current tags
            self.current_tags = self.my_text.tag_names("sel.first")
            # if statement to see tag set
            if "colored" in self.current_tags:
                self.my_text.tag_remove("colored", "sel.first", "sel.last")
            else:
                self.my_text.tag_add("colored", "sel.first", "sel.last")
    def subscript_it(self):
        # create font
        self.subscript_font = font.Font(self.my_text, self.my_text.cget("font"))
        self.subscript_font.configure(size="10")
        # configure a tag
        self.my_text.tag_configure("sub", font=self.subscript_font, offset=-4)
        # define current tags
        self.current_tags = self.my_text.tag_names("sel.first")
        # if statement to see tag set
        if "sub" in self.current_tags:
            self.my_text.tag_remove("sub", "sel.first", "sel.last")
        else:
            self.my_text.tag_add("sub", "sel.first", "sel.last")



    def specialcharacter(self,character):
        self.my_text.insert(END,character)

    def popup_bonus(self):
        self.newWindow = Toplevel(self.my_frame)
        self.newWindow.title("New Window")
        # sets the geometry of toplevel
        self.newWindow.geometry("400x400")
        #special cahracters frame
        self.specialcharframe = ttk.Labelframe(self.newWindow, text='special characters')
        self.specialcharframe.grid(row=0, column=1, sticky='ew', padx=20)
        self.list = []

        self.sql = 'select Unicode from unicode_lookbook'
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchall()
        for i in self.results:
            self.list.append(i[0])
        # declaring no. of rows
        self.row = 6
        # declaring no. of columns
        self.column = 5
        self.count = 0
        # nested loop to place buttons into rows and columns 2D array structure
        for i in range(self.row):
            for y in range(self.column):
                # check that count is less than no. of characters
                if self.count < len(self.list):
                    # place button into the window
                    ttk.Button(self.specialcharframe, text=self.list[self.count],
                               command=lambda k=self.count: self.specialcharacter(self.list[k])).grid(
                        row=i, column=y, padx=10, pady=5)
                    self.count += 1

    def add_image(self):
        #add image
        global imgToInsert
        global my_image
        # grab filename
        self.my_image = filedialog.askopenfilename(initialdir=".", title="Open File", filetypes = [("Image Files","*.png"),("Image Files","*.jpg")])
        self.imgToInsert = ImageTk.PhotoImage(file=self.my_image)
        # print(my_image)
        # self.imgToInsert=self.imgToInsert.zoom(50)
        # self.imgToInsert=self.imgToInsert.subsample(80,80)
        self.position=self.my_text.index(INSERT)
        self.my_text.image_create(self.position, image=self.imgToInsert)

    #function to save the question
    def savequestion(self):
        self.question=self.my_text.get("1.0", END)
        self.markscheme=self.my_text2.get('1.0',END)
        self.answer=self.answerspace.get()
        #check to make sure that no error occurs if a photo is not added
        if len(self.my_image) >0:
             self.image=self.my_image
        else:
            self.image=""
        self.answerchoice=self.my_text3.get('1.0',END)
        self.date=str(datetime.date.today())

        #check to make sure for paper 1 questions where no answer space is required
        self.answerspacelist=[]
        #check if answer space exist or not
        if len(self.answer)>0:
            self.answerspacelist.append(self.answer[0])
            self.answernvalue=self.answerspacelist
            self.temps=""
            # if yes, append number of lines per users selected no.of lines
            for i in range (int(self.answerspacelist[0])):
                self.temps=self.temps + "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\r\n"

            self.answer=self.temps
        #if no answer space, keep as empty string
        else:
            self.answer=""
        #sql query to search for the same question, answer choice and markscheme in database
        self.dup="select * from newpastpaper where question = '" + self.question + "'"
        self.dup2="select * from newpastpaper where mark_scheme = '" + self.markscheme + "'"
        self.dup3="select * from newpastpaper where answer_choice_paper1 = '" + self.answerchoice + "'"
        #executing sql query and collecting results into a variable
        self.mycursor.execute(self.dup)
        self.dupresults = self.mycursor.fetchall()
        self.mycursor.execute(self.dup2)
        self.dupresults2=self.mycursor.fetchall()
        self.mycursor.execute(self.dup3)
        self.dupresults3 = self.mycursor.fetchall()
        #if results for question, markscheme, answerchoice already exist in data table
        if len(self.dupresults)>0 and len(self.dupresults2)>0 and len(self.dupresults3)>0:
            #show message that it's a duplicate question
            self.dupmessage=messagebox.showerror('', 'This is a duplicate, please try again')
        else:
            #sql query to insert
            self.sql= "INSERT INTO newpastpaper VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # variables to insert into each column of a row
            self.insertvar = (0,self.question, self.answerchoice,self.markscheme,self.image, self.tempstr[5],self.tempstr[6],self.tempstr[7],
                self.tempstr[8],self.tempstr[9],self.tempstr[10],self.tempstr[11],self.tempstr[12],self.date,self.tempstr[14],self.answer,int(self.tempstr[0]))
            #SQL executing the query
            self.mycursor.execute(self.sql, self.insertvar)
            self.mydb.commit()
            #show meesagebox
            self.message = messagebox.showinfo('', 'successfully added the new question!')
            self.root.destroy()

    def getQuestion(self, questionid):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root	",
            password="",
            # port=3307,
            database="test"
        )
        self.mycursor = self.mydb.cursor()
        self.sql = "select question from newpastpaper where No = '" + questionid + "'"
        print(self.sql)
        self.mycursor.execute(self.sql)
        self.results = self.mycursor.fetchone()
        print(self.results[0])
        return (self.results[0])

    #getting all columns of the specific question (parent)
    def getAllq(self, questionid):
        #establishing databse connection
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root	",
            password="",
            # port=3307,
            database="test"
        )
        #creating a cursor
        self.mycursor = self.mydb.cursor()
        #seraching for all columns with quesion id as key
        self.sql = "select * from newpastpaper where No = '" + questionid + "'"
        #executing the search
        self.mycursor.execute(self.sql)
        #only obtain value from specific row
        self.results = self.mycursor.fetchone()
        #return the row
        return self.results