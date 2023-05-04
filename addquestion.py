from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
from tkinter import ttk
from ttkbootstrap import Style
import mysql.connector
import tkinter as tk
from PIL import Image,ImageTk
mydb = mysql.connector.connect(
        host="localhost",
        user="root	",
        password="",
        # port=3307,
        database="test"
    )
mycursor = mydb.cursor()

s = Style()
s.theme_use('lumen')
root = s.master
root.title("Add questions")
root.geometry('1400x780')
# scrollbar = Scrollbar(root)
# scrollbar.pack(side=RIGHT, fill=Y)

global open_status_name
open_status_name = False
global selected
selected = False

#create new file function
def new_file():
    #delete previous text
    my_text.delete("1.0", END)
    root.title('New file')
    status_bar.config(text="New file    ")
#open files
def open_file():
    # delete previous text
    my_text.delete("1.0", END)
    root.title('New file')
    #grab filename
    text_file=filedialog.askopenfilename(initialdir=".", title="Open File", filetypes=(("Text Files","*.txt"),("HTML Files", "*.html"), ("Python Files","*.py"),("All Files", "*")))
    #check if filenname exist
    if text_file:
        global open_status_name
        open_status_name=text_file
    #update status bar
    name=text_file
    status_bar.config(text=name)
    name=name.replace("/Users/22TinnaM","")
    root.title(name)
    #open the file
    text_file=open(text_file, 'r')
    #add file to textbox
    stuff=text_file.read()
    my_text.insert(END,stuff)
    #close file
    text_file.close()


#save as file
def save_as_file():
    text_file=filedialog.asksaveasfilename(defaultextension=".*", initialdir=".", title="Open File", filetypes=(("Text Files","*.txt"),("HTML Files", "*.html"), ("Python Files","*.py"),("All Files", "*")))
    if text_file:
        #update status bar
        name=text_file
        status_bar.config(text="Saved:"+(name))
        root.title(name)
        #save the file
        text_file=open(text_file,'w')
        text_file.write(my_text.get(1.0,END))
        #close the file
        text_file.close()
def save_file():
    global open_status_name
    if open_status_name:
        #save the file
        text_file=open(open_status_name,'w')
        text_file.write(my_text.get(1.0,END))
        #close the file
        text_file.close()
        status_bar.config(text="Saved:" + (open_status_name))
    else:
        save_as_file()
#cut text function
def cut_text(e):
    global selected
    if e:
        selected=root.clipboard_get()
    else:
        if my_text.selection_get():
            #grab selected text
            selected=my_text.selection_get()
            #delete text from text box
            my_text.delete("sel.first", "sel.last")
            # clear the clipboard then append
            root.clipboard_clear()
            root.clipboard_append(selected)

# copy text function
def copy_text(e):
    global selected
    #check if use keyboard shortcut
    if e:
        selected=root.clipboard_get()
    if my_text.selection_get():
        # grab selected text
        selected = my_text.selection_get()
        #clear the clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# copy text function
def paste_text(e):
    global selected
    if e:
        selected=root.clipboard_get()
    else:
        if selected:
            position=my_text.index(INSERT)
            my_text.insert(position, selected)

#bold function
def bold_it():
    #create font
    bold_font=font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")
    #configure a tag
    my_text.tag_configure("bold", font=bold_font)
    #define current tags
    current_tags=my_text.tag_names("sel.first")
    #if statement to see tag set
    if "bold" in current_tags:
        my_text.tag_remove("bold","sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")




def italics_it():
    # create font
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")
    # configure a tag
    my_text.tag_configure("italic", font=italics_font)
    # define current tags
    current_tags = my_text.tag_names("sel.first")
    # if statement to see tag set
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

def text_color():
    my_color=colorchooser.askcolor()[1]
    if my_color:
        status_bar.config(text=my_color)
        # create font
        color_font = font.Font(my_text, my_text.cget("font"))
        # configure a tag
        my_text.tag_configure("colored", font=color_font, foreground=my_color)
        # define current tags
        current_tags = my_text.tag_names("sel.first")
        # if statement to see tag set
        if "colored" in current_tags:
            my_text.tag_remove("colored", "sel.first", "sel.last")
        else:
            my_text.tag_add("colored", "sel.first", "sel.last")
def subscript_it():
    # create font
    subscript_font = font.Font(my_text, my_text.cget("font"))
    subscript_font.configure(size="10")
    # configure a tag
    my_text.tag_configure("sub", font=subscript_font, offset=-4)
    # define current tags
    current_tags = my_text.tag_names("sel.first")
    # if statement to see tag set
    if "sub" in current_tags:
        my_text.tag_remove("sub", "sel.first", "sel.last")
    else:
        my_text.tag_add("sub", "sel.first", "sel.last")



def specialcharacter(character):
    my_text.insert(END,character)

def popup_bonus():
    newWindow = Toplevel(my_frame)
    newWindow.title("New Window")
    # sets the geometry of toplevel
    newWindow.geometry("400x400")
    #special cahracters frame
    specialcharframe = ttk.Labelframe(newWindow, text='special characters')
    specialcharframe.grid(row=0, column=1, sticky='ew', padx=20)
    list = []

    sql = 'select Unicode from unicode_lookbook'
    mycursor.execute(sql)
    results = mycursor.fetchall()
    for i in results:
        list.append(i[0])
    print(list)
    row = 6
    column = 5
    count = 0
    for i in range(row):
        for y in range(column):
            if count < len(list):
                ttk.Button(specialcharframe, text=list[count], command=lambda k=count: specialcharacter(list[k])).grid(
                    row=i, column=y, padx=10, pady=5)
                count += 1

def add_image():
    #add image
    global imgToInsert
    global my_image
    # grab filename
    my_image = filedialog.askopenfilename(initialdir=".", title="Open File", filetypes =[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.gif")])
    imgToInsert = ImageTk.PhotoImage(file=my_image)
    # print(my_image)
    # imgToInsert=imgToInsert.zoom(50)
    # imgToInsert=imgToInsert.subsample(80,80)
    position=my_text.index(INSERT)
    my_text.image_create(position, image=imgToInsert)

#function to save the question
def savequestion():
    question=my_text.get("1.0", END)
    markscheme=my_text2.get('1.0',END)
    answer=answerspace.get()
    image=my_image

    answerspacelist=[]
    answerspacelist.append(answer[0])
    answernvalue=answerspacelist
    print(image)
    tempstr=""
    for i in range (int(answerspacelist[0])):
        tempstr=tempstr + "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\r\n"

    answer=tempstr

    sql= "INSERT INTO newpastpaper (question, mark_scheme,Answer_space, image_path) VALUES (%s, %s, %s,%s)"
    insertvar = (question,markscheme,answer,image)
    mycursor.execute(sql, insertvar)
    mydb.commit()





# create main frame
my_frame = Frame(root)
my_frame.pack(pady=5)
#-------------------------------- For questions text box
#Questions label
questionlabel=ttk.Label(my_frame, text='Question', font=('', 40))
questionlabel.pack(anchor=W,pady=5)
# create tool bar frame
toolbar_frame = ttk.Frame(my_frame)
toolbar_frame.pack(pady=5, anchor=W)
#answer space selection
answerspaceframe=ttk.Labelframe(toolbar_frame,text='answer space' )
answerspaceframe.grid(row=0, column=3,padx=10)
selected_month = tk.StringVar()
answerlines = ('2 lines', '3 lines', '4 lines', '5 lines', '6 lines')
answerspace=ttk.Combobox(answerspaceframe, textvariable=selected_month)
answerspace['values'] = answerlines
answerspace['state'] = 'readonly'  # normal
answerspace.grid(row=0, column=3, padx=5)
# Text format frame
textframe = ttk.Labelframe(toolbar_frame, text='text format')
textframe.grid(row=0, column=0, sticky='ew', padx=10)
# special charcters
specialchar = ttk.Labelframe(toolbar_frame, text='special characters')
specialchar.grid(row=0, column=1, sticky='ew', padx=10)
scbut = ttk.Button(specialchar, text='special characters', command=popup_bonus)
scbut.grid(row=0, column=0, padx=5)
textboxframe=ttk.Frame(my_frame)
textboxframe.pack(fill=BOTH,pady=5)
# create text box
my_text = Text(textboxframe, width=80, height=4, font=("Helvetica", 16),
                    selectbackground="gray",
                    selectforeground="black", undo=True,
                    wrap="none")
# create scrollbar for textbox
text_scroll = ttk.Scrollbar(textboxframe, orient='vertical', command=my_text.yview)
text_scroll.grid(row=0,  column=5, sticky='ns')
# yscrollcommand=text_scroll.set,
my_text.grid(row=0, column=0, columnspan=4, pady=5)
my_text.config(spacing1=10)  # Spacing above the first line in a block of text
my_text.config(spacing2=10)  # Spacing between the lines in a block of text
my_text.config(spacing3=10)  # Spacing after the last line in a block of text
# configure scroll bar
my_text['yscrollcommand']=text_scroll.set
#import image frame + button
importimframe=ttk.Labelframe(toolbar_frame,text="import image")
importimframe.grid(row=0, column=2, padx=10)
imagebut=ttk.Button(importimframe, text="add image", command=add_image)
imagebut.grid(row=0, column=0, padx=5)
# create menu
my_menu = Menu(root)
root.config(menu=my_menu)
#------------------------------- text box for marksheme
#marksheme label
marklabel=ttk.Label(my_frame, text='Markscheme',font=('',40))
marklabel.pack(anchor=W, pady=5)
markschemeframe=ttk.Frame(my_frame)
markschemeframe.pack(fill=BOTH, pady=5)
# create text box
my_text2 = Text(markschemeframe, width=80, height=5, font=("Helvetica", 16),
                    selectbackground="yellow",
                    selectforeground="black", undo=True,
                    wrap="none")
# create scrollbar for textbox
text_scroll2 = ttk.Scrollbar(markschemeframe, orient='vertical', command=my_text2.yview)
text_scroll2.grid(row=0,  column=5, sticky='ns')
# yscrollcommand=text_scroll.set,
my_text2.grid(row=0, column=0, columnspan=4, pady=5)
my_text2.config(spacing1=10)  # Spacing above the first line in a block of text
my_text2.config(spacing2=10)  # Spacing between the lines in a block of text
my_text2.config(spacing3=10)  # Spacing after the last line in a block of text
# configure scroll bar
my_text2['yscrollcommand']=text_scroll2.set
#--------------------------------------
savebt=ttk.Button(my_frame, text='save', style='success.TButton',command=savequestion)
savebt.pack(anchor=S, side=RIGHT)
# add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# add edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="Command-X")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="Command-C")
edit_menu.add_command(label="Paste", command=lambda: paste_text(False),
                           accelerator="Command-V")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="Command-Z")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="Shift-Command-Z")

# create status bar
status_bar = Label(root, text="ready     ", anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)

# edit bindings
root.bind('<Command-Key-x>', cut_text)
root.bind('<Command-Key-c>', copy_text)
root.bind('<Command-Key-y>', paste_text)

# create buttons
bold_button = ttk.Button(textframe, text="bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky='w', padx=5)
italics_button = ttk.Button(textframe, text="italics", command=italics_it)
italics_button.grid(row=0, column=1, sticky='w', padx=5)
undo_button = ttk.Button(textframe, text="undo", command=my_text.edit_undo)
undo_button.grid(row=0, column=2, sticky='w', padx=5)
redo_button = ttk.Button(textframe, text="redo", command=my_text.edit_redo)
redo_button.grid(row=0, column=3, sticky='w', padx=5)
color_text_button = ttk.Button(textframe, text="Text color", command=text_color)
color_text_button.grid(row=0, column=4, sticky='w', padx=5)

mainloop()
