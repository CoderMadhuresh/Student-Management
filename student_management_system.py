from tkinter import *  # importing tkinter library
from tkinter import ttk  # for using combo box
import tkinter.messagebox as mb  # for showing messages
from tkcalendar import DateEntry  # for taking entry of date
import mysql.connector as mySql  # importing mySql package


# function for creating sql database
def creatingDatabase():
    myCon = mySql.connect(host="localhost", user="root", password="password")
    cursor = myCon.cursor()
    cursor.execute('''create database if not exists student_management_system''')
    myCon.close()


creatingDatabase()


# function for creating table
def creatingTable():
    myCon = mySql.connect(host="localhost", user="root", password="password", database="student_management_system")
    cursor = myCon.cursor()
    cursor.execute('''create table if not exists students_data(
                  rollNo varchar(50),
                  name varchar(200),
                  class varchar(200),
                  dob varchar(200),
                  gender varchar(200),
                  contact varchar(200),
                  email varchar(200),
                  address varchar(200))''')
    myCon.close()


creatingTable()


# function for add students data
def add_students():
    myCon = mySql.connect(host="localhost", user="root", password="password", database="student_management_system")
    cursor = myCon.cursor()
    if not roll_val.get() or not name_val.get() or not class_val.get() or not dob_val.get() or not gender_val.get() \
            or not contact_val.get() or not email_val.get() or not address_val.get():
        mb.showerror("ERROR!", "Enter all the records to add")
    else:
        cursor.execute('''insert into students_data
                              values('{}','{}','{}',{},'{}','{}','{}','{}')'''.format(roll_val.get(), name_val.get(),
                                                                                      class_val.get(),
                                                                                      dob_val.get(), gender_val.get(),
                                                                                      contact_val.get(),
                                                                                      email_val.get(),
                                                                                      address_val.get()))
        myCon.commit()
        view_students()
        mb.showinfo("RECORD ADDED", f"Record of {name_val.get()} is added")
        clear()
        myCon.close()

    # function for showing students details


def view_students():
    myCon = mySql.connect(host="localhost", user="root", password="password", database="student_management_system")
    cursor = myCon.cursor()
    cursor.execute("select * from students_data")
    rows = cursor.fetchall()
    if len(rows) != 0:
        dataStudent.delete(*dataStudent.get_children())
        for row in rows:
            dataStudent.insert('', END, values=row)
        myCon.commit()
    myCon.close()


# function for clearing data
def clear():
    roll_val.set("")
    name_val.set("")
    class_val.set("")
    dob_val.set("")
    gender_val.set("")
    contact_val.set("")
    email_val.set("")
    address_val.set("")
    searchTxt_val.set("")
    searchBy_val.set("")


# to show details from table to frame1 columns
def getCursor(ev):
    cursorRow = dataStudent.focus()
    contents = dataStudent.item(cursorRow)
    row = contents['values']
    roll_val.set(row[0])
    name_val.set(row[1])
    class_val.set(row[2])
    dob_val.set(row[3])
    gender_val.set(row[4])
    contact_val.set(row[5])
    email_val.set(row[6])
    address_val.set(row[7])


# function for updating the details
def update():
    myCon = mySql.connect(host="localhost", user="root", password="password", database="student_management_system")
    cursor = myCon.cursor()

    if not roll_val.get() or not name_val.get() or not class_val.get() or not dob_val.get() or not gender_val.get() \
            or not contact_val.get() or not email_val.get() or not address_val.get():
        mb.showerror("ERROR!", "Enter all the records to update")

    else:
        if not roll_val.get() or not name_val.get() or not class_val.get() or not dob_val.get() \
                or not gender_val.get() or not contact_val.get() or not email_val.get() or not address_val.get():
            mb.showerror("ERROR!", "select the record to delete")

        else:
            cursor.execute('''update students_data set name=%s, class=%s, dob=%s, gender=%s, contact=%s, email=%s,
                         address=%s where rollNO=%s''',
                           (name_val.get(), class_val.get(), dob_val.get(), gender_val.get(),
                            contact_val.get(), email_val.get(), address_val.get(), roll_val.get()))
            myCon.commit()
            view_students()
            mb.showinfo("RECORD UPDATED", f"Record of {name_val.get()} is updated")
            clear()
            myCon.close()
            view_students()


# function for showing students details
def delete_data():
    myCon = mySql.connect(host="localhost", user="root", password="password", database="student_management_system")
    cursor = myCon.cursor()
    if not dataStudent.selection():
        mb.showerror("ERROR!", "Select an item to delete ")
    else:
        crt_item = dataStudent.focus()
        values = dataStudent.item(crt_item)
        selection = values["values"]
        dataStudent.delete(crt_item)
        cursor.execute("delete from students_data where rollNo=%d" % selection[0])
        myCon.commit()
        view_students()
        mb.showinfo("RECORD DELETED", f"Record of {name_val.get()} is deleted")
        clear()


# to search data
def search_data():
    myCon = mySql.connect(host="localhost", user="root", password="password", database="student_management_system")
    cursor = myCon.cursor()

    if not searchBy_val.get() or not searchTxt_val.get():
        mb.showerror("ERROR!", "Enter the field in searched by and text to search for")

    else:
        cursor.execute('''select * from students_data
                              where ''' + searchBy_val.get() + " LIKE '%" + str(searchTxt_val.get()) + "%'")
        rows = cursor.fetchall()
        if len(rows) != 0:
            dataStudent.delete(*dataStudent.get_children())
            for row in rows:
                dataStudent.insert('', END, values=row)
            myCon.commit()
        myCon.close()


win = Tk()  # defining variable of tkinter
win.geometry("1350x700+0+0")  # window size
win.title("STUDENT MANAGEMENT SYSTEM")  # window title

# All Variables to sql

roll_val = StringVar()
name_val = StringVar()
class_val = StringVar()
dob_val = StringVar()
gender_val = StringVar()
contact_val = StringVar()
email_val = StringVar()
address_val = StringVar()

searchBy_val = StringVar()
searchTxt_val = StringVar()

# top title...

title = Label(win, text="STUDENT MANAGEMENT SYSTEM", bd=3, relief=SOLID, font=("times new roman", 30, "bold"),
              highlightthickness=15, fg="crimson", bg="#fcc200").pack(side=TOP, fill=X, padx=5, pady=5)

# frame1 (short width)

frame1 = Frame(win, bd=3, relief=SOLID, bg="crimson")
frame1.place(x=5, y=93, width=355, height=605)

# frame1 title

f1Title = Label(frame1, text="MANAGE STUDENTS", font=("times new roman", 22, "bold"), fg="crimson", bg="#fcc200").grid(
    row=0, columnspan=2, pady=10)

# frame1 elements

# required details title and entry details tab

rollNo = Label(frame1, text="ROLL NUMBER - ", font=("times new roman", 12, "bold"), fg="crimson",
               bg="#fcc200", highlightthickness=1).grid(row=1, column=0, pady=10, padx=10, sticky="w")
txtRoll = Entry(frame1, textvariable=roll_val, font=("times new roman", 12), bd=5, relief=GROOVE).grid(row=1, column=1,
                                                                                                       pady=10, padx=10,
                                                                                                       sticky="w")

name = Label(frame1, text="NAME -\t\t", font=("times new roman", 12, "bold"), fg="crimson",
             bg="#fcc200",
             highlightthickness=1).grid(row=2, column=0, pady=10, padx=10, sticky="w")
txtName = Entry(frame1, textvariable=name_val, font=("times new roman", 12), bd=5, relief=GROOVE).grid(row=2, column=1,
                                                                                                       pady=10, padx=10,
                                                                                                       sticky="w")

sClass = Label(frame1, text="CLASS -\t\t", font=("times new roman", 12, "bold"), fg="crimson",
               bg="#fcc200",
               highlightthickness=1).grid(row=3, column=0, pady=10, padx=10, sticky="w")
txtClass = Entry(frame1, textvariable=class_val, font=("times new roman", 12), bd=5, relief=GROOVE).grid(row=3,
                                                                                                         column=1,
                                                                                                         pady=10,
                                                                                                         padx=10,
                                                                                                         sticky="w")

dob = Label(frame1, text="D.O.B (mm/dd/yy) -", font=("times new roman", 12, "bold"), fg="crimson",
            bg="#fcc200",
            highlightthickness=1).grid(row=4, column=0, pady=10, padx=10, sticky="w")

txtDob = DateEntry(frame1, textvariable=dob_val, font=("times new roman", 12), bd=5, relief=GROOVE). \
    grid(row=4, column=1, pady=10, padx=10, sticky="w")

gender = Label(frame1, text="GENDER -\t", font=("times new roman", 12, "bold"), fg="crimson", bg="#fcc200",
               highlightthickness=1).grid(row=5, column=0, pady=10, padx=10, sticky="w")
combo_Gender = ttk.Combobox(frame1, textvariable=gender_val, font=("times new roman", 11), state='readonly')
combo_Gender['values'] = ("Male", "Female")
combo_Gender.grid(row=5, column=1, pady=10, padx=10, sticky="w")

contact = Label(frame1, text="CONTACT NO. -\t", font=("times new roman", 12, "bold"),
                fg="crimson", bg="#fcc200",
                highlightthickness=1).grid(row=6, column=0, pady=10, padx=10, sticky="w")
txtContact = Entry(frame1, textvariable=contact_val, font=("times new roman", 12), bd=5, relief=GROOVE).grid(row=6,
                                                                                                             column=1,
                                                                                                             pady=10,
                                                                                                             padx=10,
                                                                                                             sticky="w")

email = Label(frame1, text="EMAIL ID -\t", font=("times new roman", 12, "bold"), fg="crimson",
              bg="#fcc200",
              highlightthickness=1).grid(row=7, column=0, pady=10, padx=10, sticky="w")
txtEmail = Entry(frame1, textvariable=email_val, font=("times new roman", 12), bd=5, relief=GROOVE).grid(row=7,
                                                                                                         column=1,
                                                                                                         pady=10,
                                                                                                         padx=10,
                                                                                                         sticky="w")

address = Label(frame1, text="ADDRESS -\t", font=("times new roman", 12, "bold"),
                fg="crimson", bg="#fcc200",
                highlightthickness=1).grid(row=8, column=0, pady=10, padx=10, sticky="w")
txtAddress = Entry(frame1, textvariable=address_val, font=("times new roman", 12), bd=5, relief=GROOVE).grid(row=8,
                                                                                                             column=1,
                                                                                                             pady=10,
                                                                                                             padx=10,
                                                                                                             sticky="w")

# frame of 4 CRUD buttons

buttons = Frame(frame1, bd=3, relief=SOLID, bg="crimson")
buttons.place(x=10, y=530)

createBtn = Button(buttons, text="ADD", font=("times new roman", 10, "bold"), width=7, command=add_students).grid(
    row=0, column=0, padx=10,
    pady=10)
updateBtn = Button(buttons, text="UPDATE", font=("times new roman", 10, "bold"), width=7, command=update).grid(row=0,
                                                                                                               column=1,
                                                                                                               padx=10,
                                                                                                               pady=10)
deleteBtn = Button(buttons, text="DELETE", font=("times new roman", 10, "bold"), width=7, command=delete_data).grid(
    row=0,
    column=2,
    padx=10,
    pady=10)
clearBtn = Button(buttons, text="CLEAR", font=("times new roman", 10, "bold"), width=7, command=clear).grid(row=0,
                                                                                                            column=3,
                                                                                                            padx=10,
                                                                                                            pady=10)

# frame 2 (long width)

frame2 = Frame(win, bd=3, relief=SOLID, bg="crimson")
frame2.place(x=365, y=93, width=653, height=605)

search = Label(frame2, text="SEARCH BY - ", font=("times new roman", 12, "bold"), fg="crimson", bg="#fcc200",
               highlightthickness=1).grid(row=0, column=0, pady=10, padx=5, sticky="w")
combo_search = ttk.Combobox(frame2, textvariable=searchBy_val, font=("times new roman", 14), state='readonly', width=10)
combo_search['values'] = ("rollNo", "name", "class", "dob", "gender", "contact", "email", "address")
combo_search.grid(row=0, column=1, pady=10, padx=5, sticky="w")

txtSearch = Entry(frame2, textvariable=searchTxt_val, font=("times new roman", 12), bd=5, relief=GROOVE, width=26).grid(
    row=0, column=2, pady=5,
    padx=10, sticky="w")

searchBtn = Button(frame2, text="SEARCH", font=("times new roman", 10, "bold"), width=7, command=search_data).grid(
    row=0, column=3, padx=5,
    pady=10)
showAllBtn = Button(frame2, text="SHOW ALL", font=("times new roman", 10, "bold"), width=10,
                    command=view_students).grid(row=0, column=4,
                                                padx=5, pady=10)

# details table frame in frame2

tableFrame = Frame(frame2, bd=3, relief=SOLID, bg="crimson")
tableFrame.place(x=6, y=55, width=634, height=530)

# for x and y scrolling

scrollX = Scrollbar(tableFrame, orient=HORIZONTAL)
scrollY = Scrollbar(tableFrame, orient=VERTICAL)

# treeView like structure to show data of all students

dataStudent = ttk.Treeview(tableFrame,
                           columns=("roll", "name", "class", "dob", "gender", "contact", "email", "address"),
                           xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)

# for packing and config of x and y scrolls

scrollX.pack(side=BOTTOM, fill=X)
scrollY.pack(side=RIGHT, fill=Y)
scrollX.config(command=dataStudent.xview)
scrollY.config(command=dataStudent.yview)

# assigning names to treeView structure

dataStudent.heading("roll", text="ROLL NO.")
dataStudent.heading("name", text="NAME")
dataStudent.heading("class", text="CLASS")
dataStudent.heading("dob", text="D.O.B")
dataStudent.heading("gender", text="GENDER")
dataStudent.heading("contact", text="CONTACT NO.")
dataStudent.heading("email", text="EMAIL ID")
dataStudent.heading("address", text="ADDRESS")

# showing headings

dataStudent['show'] = 'headings'
dataStudent.column("roll", width=50, anchor=CENTER)
dataStudent.column("name", width=70, anchor=CENTER)
dataStudent.column("class", width=50, anchor=CENTER)
dataStudent.column("dob", width=70, anchor=CENTER)
dataStudent.column("gender", width=50, anchor=CENTER)
dataStudent.column("contact", width=70, anchor=CENTER)
dataStudent.column("email", width=70, anchor=CENTER)
dataStudent.column("address", width=70, anchor=CENTER)
dataStudent.pack(fill=BOTH, expand=1)
dataStudent.bind("<ButtonRelease-1>", getCursor)  # to getting cursor
view_students()

win.configure(bg="#fcc200")  # window background

win.mainloop()  # running tkinter
