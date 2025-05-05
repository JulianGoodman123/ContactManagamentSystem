# ----- Imports -----
import mysql.connector
from tkinter import *

# ----- Database setup ----- 
# Created Databse and Table with columns

# ----- Connect to the MySQL server -----
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

# ----- Create a cursor object to communicate with the database -----
mycursor = db.cursor()

# If the database doesn't exist, create it
mycursor.execute("CREATE DATABASE IF NOT EXISTS contactDB")

# Tell MySQL to use the contactDB database
db.database = "contactDB"

# If the table doesn't exist, create it
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        full_name VARCHAR(255) PRIMARY KEY,
        age INT,
        contact_number VARCHAR(255),
        address TEXT
    )
""")

# Save everything we did and close the connection
db.commit()
db.close()

# ----- GUI -----

# Create Window Object
app = Tk()

# Title
app.title("Julian's Contact Management App")

# Contact Name
contact_name = StringVar()
contact_label = Label(app, text="Contact Full Name: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=0, column=0, sticky=W)
contact_entry = Entry(app, textvariable=contact_name)
contact_entry.grid(row=0, column=1)

# Contact Age
contact_age = StringVar()
contact_label = Label(app, text="Contact Age: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=0, column=2, sticky=W)
contact_entry = Entry(app, textvariable=contact_age)
contact_entry.grid(row=0, column=3)

# Contacts Contact Number
contact_number = StringVar()
contact_label = Label(app, text="Contact Number: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=1, column=0, sticky=W)
contact_entry = Entry(app, textvariable=contact_number)
contact_entry.grid(row=1, column=1)

# Contact Address
contact_address = StringVar()
contact_label = Label(app, text="Contact Address: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=1, column=2, sticky=W)
contact_entry = Entry(app, textvariable=contact_address)
contact_entry.grid(row=1, column=3)

# Contact List 











# Window Size
app.geometry("800x450")

# Program Start
app.mainloop()



# ----- Functionality -----

