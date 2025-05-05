# ===== Imports ===== #
import mysql.connector
from tkinter import *


# ===== Database Setup ===== #

# Connect to MySQL server and setup DB/table if not already there
def init_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root"
    )
    cur = db.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS contactDB")
    db.database = "contactDB"
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            full_name VARCHAR(255) PRIMARY KEY,
            age INT,
            contact_number VARCHAR(255),
            address TEXT
        )
    """)
    db.commit()
    db.close()

def run_query(query, params=(), fetch=True):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="contactDB"
    )
    cur = conn.cursor()
    cur.execute(query, params)
    
    result = cur.fetchall() if fetch else None
    if not fetch:
        conn.commit()
    
    cur.close()
    conn.close()
    return result


# ===== GUI Setup ===== #

# Create app window
app = Tk()

# Window title
app.title("Julian's Contact Management App")


# ===== Input Fields ===== #

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


# ===== Contact Info List ===== #
contacts_info = Listbox(app, height=15, width=80)
contacts_info.grid(row=3, column=0, columnspan=3, rowspan=6, pady=2, padx=20)

# Scrollbar for contact list
scrollbar = Scrollbar(app, orient=VERTICAL)
scrollbar.grid(row=3, column=3, rowspan=6, sticky='ns')
contacts_info.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=contacts_info.yview)


# ===== Functionality ===== #

def populate_list():
    contacts_info.delete(0, END)
    rows = run_query("SELECT * FROM contacts")
    for row in rows:
        contacts_info.insert(END, row)

def add_item():
    run_query(
        "INSERT INTO contacts (full_name, age, contact_number, address) VALUES (%s, %s, %s, %s)",
        (contact_name.get(), contact_age.get(), contact_number.get(), contact_address.get()),
        fetch=False
    )
    populate_list()

def delete_item():
    selected = contacts_info.get(ACTIVE)
    if selected:
        run_query("DELETE FROM contacts WHERE full_name = %s", (selected[0],), fetch=False)
        populate_list()

def update_item():
    selected = contacts_info.get(ACTIVE)
    if selected:
        run_query("""
            UPDATE contacts SET age = %s, contact_number = %s, address = %s WHERE full_name = %s
        """, (
            contact_age.get(),
            contact_number.get(),
            contact_address.get(),
            selected[0]
        ), fetch=False)
        populate_list()

def clear_text():
    contact_name.set("")
    contact_age.set("")
    contact_number.set("")
    contact_address.set("")


# ===== Buttons ===== #

create_contact = Button(app, text="Create Contact", width=12, command=add_item)
create_contact.grid(row=2, column=0, pady=20)

delete_contact = Button(app, text="Delete Contact", width=12, command=delete_item)
delete_contact.grid(row=2, column=1)

update_contact = Button(app, text="Update Contact", width=12, command=update_item)
update_contact.grid(row=2, column=2)

clear_input = Button(app, text="Clear Input Text", width=12, command=clear_text)
clear_input.grid(row=2, column=3)


# ===== App Setup and Start ===== #

# Window dimensions (adjusted for more space)
app.geometry("730x475")

# Initialize DB and populate list
init_db()
populate_list()

# Start the GUI app
app.mainloop()

# 1. Add exception handling
# 2. Write Unit tests
# 3. Write ReadMe
