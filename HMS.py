# Hospital Database Management System using Tkinter:

from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter.messagebox
from tkinter import filedialog
import pymysql
# We need pymysql connector to connect Python Script to the MySQL database
import pandas as pd


root = Tk()
root.title('"Hospital Management System" Developer ---> Sarad')
root.geometry('1390x770+50+10')
root.resizable(False,False) # for fixed window size
root.wm_iconbitmap("hospital_icon.ico")  # for window title icon


# for png logo we can direct use PhotoImage() function:
# if it is a jpg image we should import Pillow library
photo = PhotoImage(file="doctor_logo.png")
label = Label(image=photo)
label.place(x=1,y=8)

photo1 = PhotoImage(file="hospital_img.png")
label1 = Label(image=photo1)
label1.place(x=1298,y=6)


#  Assign variables for our entry field values
P_ID_var = StringVar()
Name_var = StringVar()
DOB_var = StringVar()
Gender_var = StringVar()
Age_var = StringVar()
Email_var = StringVar()
Address_var = StringVar()
Contact_var = StringVar()
Relatives_var = StringVar()
Insurance_var = StringVar()
BloodGrp_var = StringVar()
Diagnosis_var = StringVar()
ReferredTo_var = StringVar()
# we use StringVar() even for data like ID, Contacts etc insted of intVar() cuz we don't need to perform any types of calculations here
# we just have to enter data so StringVar() works for all


# create functions for different button actions:

# function for closing the program
def quitapp():
    quitapp = tkinter.messagebox.askyesno("Hospital Management System", "Do you want to exit?")
    if quitapp > 0:
        # if user presses yes button it represents True which means value 1 in boolean so it's greater than 0;
        # thus destroy() function executes but if user clicks no program does not close as destroy() doesnot execute
        root.destroy()
        return


# function to create a new database:

#Note: we will connect to the database using host, username and password of MySQL. If you don't remember your username or password, create a new user with a password.
def create_database():
    ## connecting to the database using 'connect()' method
    ## it takes 3 required parameters 'host', 'user', 'password'
    try:
        conn= pymysql.connect(host="localhost",
                              user="root",
                              password="SaRad@My#SQL@7319")

        ## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
        cursor = conn.cursor()

    except:
        return

    try:
        ## creating a databse called 'patients_database'
        ## 'execute()' method is used to compile a 'SQL' statement
        cd = 'create database patients_database'
        cursor.execute(cd)
        cd = 'use patients_database'
        cursor.execute(cd)

        #Now Use the create table table_name to create a table in the selected database.
        # Note: Primary Key:- It is a unique value in the table. It helps to find each row uniquely in the table.

        # To create a Primary Key, we use the PRIMARY KEY statement while creating the table.
        cd = 'create table pinfo5 (patient_id int primary key not null ,full_name varchar(100) not null,dob varchar(100) not null ,gender varchar(100) not null ,age int not null ,email varchar(100) not null,address varchar(100) not null ,contact_no varchar(100) not null ,relatives_name varchar(100) not null,health_insurance varchar(100) not null,blood_group varchar(100) not null,diagnosis varchar(100) not null,referred_to varchar(100) not null)'
        ## getting all the tables which are present in 'datacamp' database
        cursor.execute(cd)
    # if there is already that database with same name we will be using the same
    except:
        cd= 'use patients_database'
        cursor.execute(cd)
create_database()


# function to add new records to the database
def add_Patients():
    if P_ID_var.get() == "" or Name_var.get()=="" or DOB_var.get() == "" or Gender_var.get() == "" or Age_var.get() == "" or Email_var.get() == "" or Address_var.get() == "" or Contact_var.get() == "" or Relatives_var.get() == "" or Insurance_var.get() == "" or BloodGrp_var.get() == "" or Diagnosis_var.get() == "" or ReferredTo_var.get() == "" :
        tkinter.messagebox.showerror("Error",'All fields are required!')
    else:

        conn= pymysql.connect(host="localhost",
                              user="root",
                              password="SaRad@My#SQL@7319",database="patients_database")
        cursor= conn.cursor()
        # now we check if that id is already present in the database or not...if it is present then user gets error message else record is created successfully

        # Inserting data into table to store it. Use INSERT INTO table_name (column_names) VALUES (data) statement to insert into the table.
        try:
            cursor.execute("insert into pinfo5 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(P_ID_var.get(),Name_var.get(),DOB_var.get(),Gender_var.get(),Age_var.get(),Email_var.get(),Address_var.get(),Contact_var.get(),Relatives_var.get(),Insurance_var.get(),BloodGrp_var.get(),Diagnosis_var.get(),ReferredTo_var.get()))

        # to make final changes we have to run the 'commit()' method of the database object
            conn.commit()

        except:
            tkinter.messagebox.showerror('Error',f'This ID  {P_ID_var.get()} already exists..create another ID ')
            cursor.execute("insert into pinfo5 values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (P_ID_var.get(), Name_var.get(), DOB_var.get(), Gender_var.get(), Age_var.get(), Email_var.get(),
            Address_var.get(), Contact_var.get(), Relatives_var.get(), Insurance_var.get(), BloodGrp_var.get(),
            Diagnosis_var.get(), ReferredTo_var.get()))
            conn.commit()

        conn.close()
        tkinter.messagebox.showinfo("Success",f"Record for id {P_ID_var.get()} added successfully!")


# now let's create a function to fetch data from database and display it in our gui section:
def fetch_data():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="SaRad@My#SQL@7319", database="patients_database")
    cursor = conn.cursor()
    # To retrieve the data from a table we use, SELECT column_names FROM table_name statement.
    # To get all records from a table, we use * in place of column names
    cursor.execute("select * from pinfo5")
    rows= cursor.fetchall() # 'fetchall()' method fetches all the rows from the last executed statement
    #  it returns a list of all databases present

    if len(rows) !=0: # if length of rows is not equal to 0 than there is some data in it;so we fetch that data
        Patient_table.delete(*Patient_table.get_children())
        ## Showing the data
        for row in rows:
            Patient_table.insert('',END,values=row)
            conn.commit()

    conn.close()


# function to clear the data in the entry form:
def clearData():
    entry_Id.delete(0,END)
    entry_name.delete(0,END)
    entry_dob.delete(0,END)
    entry_gender.delete(0,END)
    entry_age.delete(0,END)
    entry_email.delete(0,END)
    entry_address.delete(0,END)
    entry_contact_no.delete(0,END)
    entry_relatives.delete(0,END)
    entry_health_insurance.delete(0,END)
    entry_blood_grp.delete(0,END)
    entry_diagnosis.delete(0,END)
    entry_referred.delete(0,END)


# Now lets create a function to show data inside the entry field when user clicks on the particular row of that table list:
# for that we have to bind this get_cursor_data with the Patient_table
# (i.e when user clicks on that row ; then get_cursor_data() function gets executed) ----> it is concept of event handling

def get_cursor_data(event):
    cursor_row = Patient_table.focus() # when user clicks on that row ; focus() sends that row inside cursor_row
    contents = Patient_table.item(cursor_row) # Every items inside that cursor_row now goes into contents
    row = contents['values'] # we now fetch all values from contents
    entry_Id.delete(0,END)
    entry_Id.insert(END,row[0])
    entry_name.delete(0,END)
    entry_name.insert(END, row[1])
    entry_dob.delete(0,END)
    entry_dob.insert(END, row[2])
    entry_gender.delete(0,END)
    entry_gender.insert(END, row[3])
    entry_age.delete(0,END)
    entry_age.insert(END, row[4])
    entry_email.delete(0,END)
    entry_email.insert(END, row[5])
    entry_address.delete(0,END)
    entry_address.insert(END, row[6])
    entry_contact_no.delete(0,END)
    entry_contact_no.insert(END, row[7])
    entry_relatives.delete(0,END)
    entry_relatives.insert(END, row[8])
    entry_health_insurance.delete(0,END)
    entry_health_insurance.insert(END, row[9])
    entry_blood_grp.delete(0,END)
    entry_blood_grp.insert(END, row[10])
    entry_diagnosis.delete(0,END)
    entry_diagnosis.insert(END, row[11])
    entry_referred.delete(0,END)
    entry_referred.insert(END, row[12])


# function to update the already existing data inside database:
def updateData():

    conn= pymysql.connect(host="localhost",
                          user="root",
                          password="SaRad@My#SQL@7319",database="patients_database")
    cursor= conn.cursor()
    # UPDATE keyword is used to update the data of a record or records.
    # UPDATE table_name SET column_name = new_value WHERE condition statement is used to update the value of a specific row.

    cursor.execute("update pinfo5 set full_name=%s,dob=%s,gender=%s,age=%s,email=%s,address=%s,contact_no=%s,relatives_name=%s,health_insurance=%s,blood_group=%s,diagnosis=%s,referred_to=%s where patient_id=%s",(Name_var.get(),DOB_var.get(),Gender_var.get(),Age_var.get(),Email_var.get(),Address_var.get(),Contact_var.get(),Relatives_var.get(),Insurance_var.get(),BloodGrp_var.get(),Diagnosis_var.get(),ReferredTo_var.get(),P_ID_var.get()))

    conn.commit()
    fetch_data() # we call fetch_data function so that changes made is reflected automatically inside the table box
    tkinter.messagebox.showinfo("Success", f"Record for Id {P_ID_var.get()} updated successfully!")
    conn.close()


# function for deleting data from database:
def delete_data():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="SaRad@My#SQL@7319", database="patients_database")
    cursor = conn.cursor()
    # DELETE keyword is used to delete the records from the table.
    # DELETE FROM table_name WHERE condition statement is used to delete records. If you don't specify the condition, then all of the records will be deleted.

    # SELECT column_name FROM table_name WHERE condition statement will be used to retrieve the data on some condition.
    cursor.execute("delete from pinfo5 where patient_id=%s",P_ID_var.get())
    conn.commit()
    clearData()
    fetch_data()
    tkinter.messagebox.showinfo("Success", "Record deleted successfully!")
    conn.close()


# function to search the contents inside database:
def searchData():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="SaRad@My#SQL@7319",database="patients_database")
    cursor = conn.cursor()
    cursor.execute("select * from pinfo5 where patient_id=%s or full_name=%s or dob=%s or gender=%s or age=%s or email=%s or address=%s or contact_no= %s or relatives_name=%s or health_insurance=%s or blood_group=%s or diagnosis=%s or referred_to=%s",(entry_Id.get(),entry_name.get(),entry_dob.get(),entry_gender.get(),entry_age.get(),entry_email.get(),entry_address.get(),entry_contact_no.get(),entry_relatives.get(),entry_health_insurance.get(),entry_blood_grp.get(),entry_diagnosis.get(),entry_referred.get(),))
    rows= cursor.fetchall()
    Patient_table.delete(* Patient_table.get_children())

    for row in rows:
        sd= [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]]
        Patient_table.insert('', END, values=sd)

    conn.close()


# now let's create a function to export our data as a csv file:
# for that we import panda library and we the data frame tool inside it to export our database as a csv file

def export_data():
    var1 = filedialog.asksaveasfilename() # opens save as dialog box
    var2 = Patient_table.get_children()
    id,name,dob,gender,age,email,address,contact,relatives,insurance,bloodgrp,diagnosis,referredto=[],[],[],[],[],[],[],[],[],[],[],[],[]
    for i in var2:
        contents = Patient_table.item(i)
        var3 = contents['values']
        id.append(var3[0]),name.append(var3[1]),dob.append(var3[2]),gender.append(var3[3]),age.append(var3[4]),email.append(var3[5]),address.append(var3[6]),contact.append(var3[7]),relatives.append(var3[8]),insurance.append(var3[9]),bloodgrp.append(var3[10]),diagnosis.append(var3[11]),referredto.append(var3[12])
    data = ['Id','Name','DOB','Gender','Age','Email','Address','Contact','Relatives Name','Insurance','Blood Group','Diagnosis','Referred To']
    data_frame = pd.DataFrame(list(zip(id,name,dob,gender,age,email,address,contact,relatives,insurance,bloodgrp,diagnosis,referredto)),columns=data)
    paths = f'{var1}.csv'
    data_frame.to_csv(paths,index=False)
    tkinter.messagebox.showinfo('Notifications', f'Patients data saved successfully in {paths}')


# lets now create title of our project:
# we make the text inside our title frame to slide
# for that we implement the logic as:

top = 'Hospital Database Management System'
counter = 0 # counter increases every time a letter is added into text variable from top variable
text = ''

def Slider_func():
    global counter,text
    if(counter>=len(top)): # counter resets from 0 if its value becomes greater than length of string inside top variable
        counter = 0
        text = ''
        Slider_Label.config(text=text)
    else:
        text = text+top[counter]
        Slider_Label.config(text=text)
        counter += 1
    Slider_Label.after(250,Slider_func) # slider function is called after every 210 microseconds until every character inside top variable is executed

Slider_Label = Label(root,text=top,font='Georgia 38 italic bold ',relief=SUNKEN,bg='#f77fab',fg='black',bd=10,pady=8)
Slider_Label.place(x=92,y=3,width=1199)
Slider_func() # function called


# Now let's create a frame in our root window for registration of new patients:

Infoframe = Frame(root,bd=5,relief=RIDGE,bg='#9ad5de')
Infoframe.place(x=2,y=108,width=450,height=563)

info_title=Label(Infoframe,text='Register New Patients',font='times 20 bold',bg='crimson',fg='white')
info_title.place(x=1,y=1,width=438,height=35)


# let's create entry widget now:

# entry for patient's ID:
label_Id= Label(Infoframe,text='Patient ID',font='times 15 bold',bg="#9ad5de")
label_Id.place(x=10,y=52)

entry_Id=Entry(Infoframe,textvariable=P_ID_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_Id.place(x=170,y=51,width=240,height=28)


# entry for patient's full name:
label_name= Label(Infoframe,text='Full Name',font='Times 15 bold',bg="#9ad5de")
label_name.place(x=10,y=90)

entry_name=Entry(Infoframe,textvariable=Name_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_name.place(x=170,y=90,width=240,height=28)


# entry for patient's date of birth:
label_dob= Label(Infoframe,text='D.O.B',font='Times 15 bold',bg="#9ad5de")
label_dob.place(x=10,y=131)


entry_dob = DateEntry(Infoframe,textvariable=DOB_var,background='#F0F26B',foreground='#85929E', borderwidth=1,font='times 12',relief=GROOVE)
entry_dob.place(x=170,y=129,width=240,height=28)


# entry for patient's gender:
label_gender= Label(Infoframe,text='Gender',font='Times 15 bold',bg="#9ad5de")
label_gender.place(x=10,y=169)


# let's use combobox widget for gender rather than a simple entry widget
# for that we import ttk from tkinter
entry_gender = ttk.Combobox(Infoframe,textvariable=Gender_var,font='Helvetica 11')
entry_gender['values'] =('Male','Female','Other')
entry_gender.place(x=170,y=168,width=240,height=28)


# entry for patient's age:
label_age= Label(Infoframe,text='Age',font='Times 15 bold',bg="#9ad5de")
label_age.place(x=10,y=206)


entry_age = Spinbox(root,textvariable=Age_var, from_=1, to=100,font='times 12',bd=1,relief=SUNKEN)
entry_age.place(x=176,y=318,width=240,height=28)


# entry for patient email id:

label_email= Label(Infoframe,text='Email',font='Times 15 bold',bg="#9ad5de")
label_email.place(x=10,y=248)

entry_email=Entry(Infoframe,textvariable=Email_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_email.place(x=170,y=244,width=240,height=28)

# entry for patient address:

label_address= Label(Infoframe,text='Address',font='Times 15 bold',bg="#9ad5de")
label_address.place(x=10,y=286)

entry_address=Entry(Infoframe,textvariable=Address_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_address.place(x=170,y=283,width=240,height=28)

# entry for patient Contact No:

label_contact_no= Label(Infoframe,text='Contact No.',font='Times 15 bold',bg="#9ad5de")
label_contact_no.place(x=10,y=323)

entry_contact_no=Entry(Infoframe,textvariable=Contact_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_contact_no.place(x=170,y=321,width=240,height=28)

# entry for relatives name:

label_relatives= Label(Infoframe,text='Relatives Name',font='Times 15 bold',bg="#9ad5de")
label_relatives.place(x=10,y=360)

entry_relatives=Entry(Infoframe,textvariable=Relatives_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_relatives.place(x=170,y=360,width=240,height=28)

# entry for health insurance:

label_health_insurance= Label(Infoframe,text='Health Insurance',font='Times 15 bold',bg="#9ad5de")
label_health_insurance.place(x=10,y=398)

entry_health_insurance = ttk.Combobox(Infoframe,textvariable=Insurance_var,font='Helvetica 11')
entry_health_insurance['values'] =('Yes','No')
entry_health_insurance.place(x=170,y=398,width=240,height=28)

# entry for patient Blood Group:

label_blood_grp= Label(Infoframe,text='Blood Group',font='Times 15 bold',bg="#9ad5de")
label_blood_grp.place(x=10,y=437)

entry_blood_grp = ttk.Combobox(Infoframe,textvariable=BloodGrp_var,font='Helvetica 11')
entry_blood_grp['values'] =('A +ve','A -ve','B +ve','B -ve','O +ve','O -ve','AB +ve','AB -ve')
entry_blood_grp.place(x=170,y=436,width=240,height=28)

# entry for diagnosis:

label_diagnosis= Label(Infoframe,text='Diagnosis',font='Times 15 bold',bg="#9ad5de")
label_diagnosis.place(x=10,y=475)

entry_diagnosis=Entry(Infoframe,textvariable=Diagnosis_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_diagnosis.place(x=170,y=474,width=240,height=28)

# entry for referred to:
label_referred= Label(Infoframe,text='Referred To',font='Times 15 bold',bg="#9ad5de")
label_referred.place(x=10,y=513)

entry_referred=Entry(Infoframe,textvariable=ReferredTo_var,font='Helvetica 11',bd=1,relief=GROOVE)
entry_referred.place(x=170,y=512,width=240,height=28)


# For buttons:
# first import images of buttons:
Add_image = PhotoImage(file="Add_img.png")
image_label1 = Label(image=Add_image)

Display_image = PhotoImage(file="Display_img.png")
image_label2 = Label(image=Display_image)

Clear_image = PhotoImage(file="Clear_img.png")
image_label3 = Label(image=Clear_image)

Update_image = PhotoImage(file="Update_img.png")
image_label4 = Label(image=Update_image)

Delete_image = PhotoImage(file="Delete_img.png")
image_label5 = Label(image=Delete_image)

Search_image = PhotoImage(file="Search_img.png")
image_label6 = Label(image=Search_image)

Export_image = PhotoImage(file="Export_img.png")
image_label7 = Label(image=Export_image)

Exit_image = PhotoImage(file="Exit_img.png")
image_label8 = Label(image=Exit_image)


# Now here instead of text attribute we directly pass image attribute inside button() function
# so that image is passed inside that button
# now we make borderwidth=0 to remove extra spaces outside that image; so that it now looks like an actual button
buttonAdd = Button(root,image=Add_image, bd=0,command=add_Patients)
buttonAdd.place(x=6,y=687,width=175,height=75)

buttonDisplayData = Button(root,image=Display_image, bd=0,command=fetch_data)
buttonDisplayData.place(x=190,y=687,width=175,height=75)

buttonClear = Button(root,image=Clear_image, bd=0,command=clearData)
buttonClear.place(x=375,y=687,width=175,height=75)

buttonUpdate = Button(root, image = Update_image,bd=0,command=updateData)
buttonUpdate.place(x=560,y=687,width=175,height=75)

buttonDelete = Button(root,image=Delete_image,  bd=0,command=delete_data)
buttonDelete.place(x=745,y=687,width=175,height=75)

buttonSearch = Button(root,image=Search_image, bd=0,command=searchData)
buttonSearch.place(x=930,y=687,width=175,height=75)

buttonExport = Button(root,image=Export_image, bd=0,command=export_data)
buttonExport.place(x=1115,y=687,width=175,height=75)

buttonQuit = Button(root,image=Exit_image, bd=0, command=quitapp)
buttonQuit.place(x=1300,y=687,width=80,height=76)


# Lets now create a separate frame for displaying database contents inside our gui:
Detailsframe = Frame(root,bd=5,relief=RIDGE,bg='#40bf80')
Detailsframe.place(x=470,y=108,width=917,height=563)

info_title=Label(Detailsframe,text='Patient Details',font='times 20 bold',bg='crimson',fg='white')
info_title.place(x=1,y=1,width=905,height=35)


# Table frame for patient details:

TableData_frame = Frame(Detailsframe,bd=7,relief=SUNKEN,bg='black')
TableData_frame.place(x=10,y=48,width=888,height=496)

style = ttk.Style()
style.configure('Treeview.Heading',font='times 14 bold ',foreground='#0000e6')
style.configure('Treeview',font='times 11 bold italic',background='#9ad5de',foreground='black')

scrollbar_x= Scrollbar(TableData_frame,orient=HORIZONTAL) # orient specifies the direction where scroll bar is to be set
scrollbar_y= Scrollbar(TableData_frame,orient=VERTICAL)
Patient_table = ttk.Treeview(TableData_frame,columns=('ID','Name','DOB','Gender','Age','Email','Address','Contact','Relatives','Insurance','BloodGrp','Diagnosis','ReferredTo'),xscrollcommand = scrollbar_x.set,yscrollcommand = scrollbar_y.set)

scrollbar_x.pack(side=BOTTOM,fill=X)
scrollbar_y.pack(side=RIGHT,fill=Y)
scrollbar_x.config(command=Patient_table.xview)
scrollbar_y.config(command=Patient_table.yview)
Patient_table.heading('ID',text='Patient ID')
Patient_table.heading('Name',text='Full Name')
Patient_table.heading('DOB',text='D.O.B')
Patient_table.heading('Gender',text='Gender')
Patient_table.heading('Age',text='Age')
Patient_table.heading('Email',text='Email')
Patient_table.heading('Address',text='Address')
Patient_table.heading('Contact',text='Contact No.')
Patient_table.heading('Relatives',text='Relatives Name')
Patient_table.heading('Insurance',text='Health Insurance')
Patient_table.heading('BloodGrp',text='Blood group')
Patient_table.heading('Diagnosis',text='Diagnosis')
Patient_table.heading('ReferredTo',text='Referred To')
Patient_table['show'] ='headings'  # for displaying title only
Patient_table.pack(fill=BOTH,expand=True)  # we do expand=True so that it adjusts fully according to the frame

# here let's bind Patient_table and call get_cursor_data() function inside it:

Patient_table.bind("<ButtonRelease-1>",get_cursor_data)

# to set the width of the headings as required:
Patient_table.column('ID',width=100)
Patient_table.column('Name',width=190)
Patient_table.column('DOB',width=125)
Patient_table.column('Gender',width=100)
Patient_table.column('Age',width=100)
Patient_table.column('Email',width=190)
Patient_table.column('Address',width=190)
Patient_table.column('Contact',width=125)
Patient_table.column('Relatives',width=190)
Patient_table.column('Insurance',width=135)
Patient_table.column('BloodGrp',width=125)
Patient_table.column('Diagnosis',width=125)
Patient_table.column('ReferredTo',width=190)


root.mainloop()