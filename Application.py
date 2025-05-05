# ----- Imports ----- #
import mysql.connector
from tkinter import *



# ===== Database Setup ===== #

# Connect to MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

# Create cursor to interact with DB
mycursor = db.cursor()

# Create DB if it doesn’t exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS contactDB")

# Select the DB
db.database = "contactDB"

# Create contacts table if it doesn’t exist
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        full_name VARCHAR(255) PRIMARY KEY,
        age INT,
        contact_number VARCHAR(255),
        address TEXT
    )
""")

# Commit changes and close connection
db.commit()
db.close()



# ===== GUI Setup ===== #

# Create app window
app = Tk()

# Window title
app.title("Julian's Contact Management App")

# ----- Contact Name ----- #
contact_name = StringVar()
contact_label = Label(app, text="Contact Full Name: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=0, column=0, sticky=W)
contact_entry = Entry(app, textvariable=contact_name)
contact_entry.grid(row=0, column=1)

# ----- Contact Age ----- #
contact_age = StringVar()
contact_label = Label(app, text="Contact Age: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=0, column=2, sticky=W)
contact_entry = Entry(app, textvariable=contact_age)
contact_entry.grid(row=0, column=3)

# ----- Contact Number ----- #
contact_number = StringVar()
contact_label = Label(app, text="Contact Number: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=1, column=0, sticky=W)
contact_entry = Entry(app, textvariable=contact_number)
contact_entry.grid(row=1, column=1)

# ----- Contact Address ----- #
contact_address = StringVar()
contact_label = Label(app, text="Contact Address: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=1, column=2, sticky=W)
contact_entry = Entry(app, textvariable=contact_address)
contact_entry.grid(row=1, column=3)

# ----- Contact Info List ----- #
contacts_info = Listbox(app, height=8, width=50)
contacts_info.grid(row=3, column=0, columnspan=3, rowspan=6, pady=2, padx=20)

# Scrollbar for contact list
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
contacts_info.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=contacts_info.yview)



# ===== Functionality ===== #

def populate_list():
    print("Populate")

def add_item():
    print("add")

def delete_item():
    print("del")

def update_item():
    print("update")
    
def clear_text():
    print("clear")



# ===== Buttons ===== #

create_contact = Button(app, text="Create Contact", width=12, command=add_item)
create_contact.grid(row=2, column=0, pady=20)

delete_contact = Button(app, text="Delete Contact", width=12, command=delete_item)
delete_contact.grid(row=2, column=1)

update_contact = Button(app, text="Update Contact", width=12, command=update_item)
update_contact.grid(row=2, column=2)

clear_input = Button(app, text="Clear Input Text", width=12, command=clear_text)
clear_input.grid(row=2, column=3)



# Window dimensions
app.geometry("650x450")

# Populate Table on Load
populate_list()

# Start the GUI app
app.mainloop()
