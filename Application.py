# ===== Imports ===== #
import mysql.connector
from tkinter import *
from tkinter import ttk


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
contact_label = Label(app, text="Full Name: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=0, column=0, sticky=W)
contact_entry = Entry(app, textvariable=contact_name)
contact_entry.grid(row=0, column=1)

# ----- Contact Age ----- #
contact_age = StringVar()
contact_label = Label(app, text="Age: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=0, column=2, sticky=W)
contact_entry = Entry(app, textvariable=contact_age)
contact_entry.grid(row=0, column=3)

# ----- Contact Number ----- #
contact_number = StringVar()
contact_label = Label(app, text="Number: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=1, column=0, sticky=W)
contact_entry = Entry(app, textvariable=contact_number)
contact_entry.grid(row=1, column=1)

# ----- Contact Address ----- #
contact_address = StringVar()
contact_label = Label(app, text="Address: ", font=('bold', 14), pady=20, padx=10)
contact_label.grid(row=1, column=2, sticky=W)
contact_entry = Entry(app, textvariable=contact_address)
contact_entry.grid(row=1, column=3)


# ===== Contact Info Treeview with Headers ===== #
# Treeview (table) to display contact info
columns = ("Full Name", "Age", "Contact Number", "Address")

tree = ttk.Treeview(app, columns=columns, show="headings", height=10)
tree.grid(row=3, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

# Column headers
tree.heading("Full Name", text="Full Name", anchor=W)
tree.heading("Age", text="Age", anchor=W)
tree.heading("Contact Number", text="Contact Number", anchor=W)
tree.heading("Address", text="Address", anchor=W)

# Set column widths (optional, you can adjust as needed)
tree.column("Full Name", width=180)
tree.column("Age", width=60)
tree.column("Contact Number", width=180)
tree.column("Address", width=250)


# Scrollbar for Treeview
scrollbar = Scrollbar(app, orient=VERTICAL, command=tree.yview)
scrollbar.grid(row=3, column=4, rowspan=6, sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)


# ===== Functionality ===== #

def populate_treeview():
    # Clear current entries in treeview
    for row in tree.get_children():
        tree.delete(row)

    rows = run_query("SELECT * FROM contacts")
    for row in rows:
        tree.insert("", "end", values=row)

def add_item():
    run_query(
        "INSERT INTO contacts (full_name, age, contact_number, address) VALUES (%s, %s, %s, %s)",
        (contact_name.get(), contact_age.get(), contact_number.get(), contact_address.get()),
        fetch=False
    )
    populate_treeview()
    clear_text()

def delete_item():
    selected_item = tree.selection()
    if selected_item:
        selected_contact = tree.item(selected_item)["values"][0]
        run_query("DELETE FROM contacts WHERE full_name = %s", (selected_contact,), fetch=False)
        populate_treeview()
        clear_text()

def update_item():
    selected_item = tree.selection()
    if selected_item:
        selected_contact = tree.item(selected_item)["values"][0]
        run_query(""" 
            UPDATE contacts SET age = %s, contact_number = %s, address = %s WHERE full_name = %s
        """, (
            contact_age.get(),
            contact_number.get(),
            contact_address.get(),
            selected_contact
        ), fetch=False)
        populate_treeview()


def clear_text():
    contact_name.set("")
    contact_age.set("")
    contact_number.set("")
    contact_address.set("")

# ===== Double Click Event Handler ===== #

def on_item_double_click(event):
    # Get selected item from treeview
    selected_item = tree.selection()
    if selected_item:
        # Get values of the selected row
        values = tree.item(selected_item)["values"]
        
        # Populate the input fields with the selected row data
        contact_name.set(values[0])  # Full Name
        contact_age.set(values[1])  # Age
        contact_number.set(values[2])  # Contact Number
        contact_address.set(values[3])  # Address


# Bind double-click event to the Treeview
tree.bind("<Double-1>", on_item_double_click)


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
app.geometry("800x475")

# Initialize DB and populate treeview
init_db()
populate_treeview()

# Start the GUI app
app.mainloop()

# 1. Add exception handling
# 2. Write and test Unit tests
# 3. Write ReadMe without executable
# 4. If not doing executable, remove files we don't need
