# ===== Imports ===== #
import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re


# ===== Database Setup ===== #

def init_db():
    try:
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
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                age INT,
                phone VARCHAR(255) UNIQUE,
                address TEXT,
                PRIMARY KEY (phone)
            )
        """)
        db.commit()
        db.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error initializing database: {err}")


def run_query(query, params=(), fetch=True):
    """Executes a query with parameters and fetches results if required."""
    try:
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
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error executing query: {err}")
        return []


# ===== GUI Setup ===== #

# Create app window
app = Tk()
app.title("Julian's Contact Management App")

# ===== Input Fields ===== #

# ----- Contact First Name ----- #
first_name = StringVar()
Label(app, text="First Name: ", font=('bold', 14), pady=5, padx=10).grid(row=0, column=0, sticky=W)
first_name_entry = Entry(app, textvariable=first_name)
first_name_entry.grid(row=0, column=1, padx=5, pady=5)

# ----- Contact Last Name ----- #
last_name = StringVar()
Label(app, text="Last Name: ", font=('bold', 14), pady=5, padx=10).grid(row=0, column=2, sticky=W)
last_name_entry = Entry(app, textvariable=last_name)
last_name_entry.grid(row=0, column=3, padx=5, pady=5)

# ----- Contact Age ----- #
age = IntVar()
Label(app, text="Age: ", font=('bold', 14), pady=5, padx=10).grid(row=1, column=0, sticky=W)
age_entry = Entry(app, textvariable=age)
age_entry.grid(row=1, column=1, padx=5, pady=5)

# ----- Contact Phone ----- #
phone = StringVar()
Label(app, text="Phone: ", font=('bold', 14), pady=5, padx=10).grid(row=1, column=2, sticky=W)
phone_entry = Entry(app, textvariable=phone)
phone_entry.grid(row=1, column=3, padx=5, pady=5)

# ----- Contact Address ----- #
address = StringVar()
Label(app, text="Address: ", font=('bold', 14), pady=5, padx=10).grid(row=2, column=0, sticky=W)
address_entry = Entry(app, textvariable=address)
address_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)


# ===== Search Section ===== #

search_var = StringVar()
Label(app, text="Search by First Name: ", font=('bold', 14), pady=5, padx=10).grid(row=3, column=0, sticky=W)
search_entry = Entry(app, textvariable=search_var)
search_entry.grid(row=3, column=1, padx=5, pady=5)

search_button = Button(app, text="Search", width=12, command=lambda: search_item())
search_button.grid(row=3, column=2, padx=5, pady=5)


# ===== Contact Info Treeview with Headers ===== #
columns = ("First Name", "Last Name", "Age", "Phone", "Address")

tree = ttk.Treeview(app, columns=columns, show="headings", height=10)
tree.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

# Column headers
tree.heading("First Name", text="First Name", anchor=W)
tree.heading("Last Name", text="Last Name", anchor=W)
tree.heading("Age", text="Age", anchor=W)
tree.heading("Phone", text="Phone", anchor=W)
tree.heading("Address", text="Address", anchor=W)

# Set column widths
tree.column("First Name", width=150)
tree.column("Last Name", width=150)
tree.column("Age", width=60)
tree.column("Phone", width=200)
tree.column("Address", width=300)


# Scrollbar for Treeview
scrollbar = Scrollbar(app, orient=VERTICAL, command=tree.yview)
scrollbar.grid(row=4, column=4, rowspan=6, sticky='ns', pady=20)
tree.configure(yscrollcommand=scrollbar.set)


# ===== Functionality ===== #

def populate_treeview():
    """Populate the Treeview with contacts from the database."""
    for row in tree.get_children():
        tree.delete(row)

    rows = run_query("SELECT * FROM contacts")
    if not rows:
        messagebox.showinfo("No Contacts", "No contacts found in the database.")
    
    for row in rows:
        tree.insert("", "end", values=row)


def add_item():
    """Add a new contact to the database."""
    if not validate_inputs():
        return
    
    try:
        run_query(
            "INSERT INTO contacts (first_name, last_name, age, phone, address) VALUES (%s, %s, %s, %s, %s)",
            (first_name.get(), last_name.get(), age.get(), phone.get(), address.get()),
            fetch=False
        )
        populate_treeview()
        clear_text()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add contact: {e}")


def delete_item():
    """Delete the selected contact from the database."""
    selected_item = tree.selection()
    if selected_item:
        selected_contact = tree.item(selected_item)["values"][3]  # Phone number is unique
        run_query("DELETE FROM contacts WHERE phone = %s", (selected_contact,), fetch=False)
        populate_treeview()
        clear_text()


def update_item():
    """Update the selected contact's details in the database."""
    selected_item = tree.selection()
    if selected_item:
        selected_contact = tree.item(selected_item)["values"][3]  # Phone number is unique
        
        # Prepare the data to update
        first_name_val = first_name.get() if first_name.get() else tree.item(selected_item)["values"][0]
        last_name_val = last_name.get() if last_name.get() else tree.item(selected_item)["values"][1]
        age_val = age.get() if age.get() else tree.item(selected_item)["values"][2]
        address_val = address.get() if address.get() else tree.item(selected_item)["values"][4]
        
        run_query(""" 
            UPDATE contacts SET first_name = %s, last_name = %s, age = %s, address = %s WHERE phone = %s
        """, (
            first_name_val,
            last_name_val,
            age_val,
            address_val,
            selected_contact
        ), fetch=False)
        populate_treeview()


def clear_text():
    """Clear all input fields."""
    first_name.set("")
    last_name.set("")
    age.set("")
    phone.set("")
    address.set("")


def validate_inputs():
    """Validate the inputs to ensure no spaces and all fields are filled."""
    if not all([first_name.get(), last_name.get(), age.get(), phone.get(), address.get()]):
        messagebox.showerror("Input Error", "All fields are required.")
        return False

    if ' ' in first_name.get() or ' ' in last_name.get() or ' ' in phone.get():
        messagebox.showerror("Input Error", "First Name, Last Name, and Phone should not contain spaces.")
        return False

    if not phone.get().isdigit():
        messagebox.showerror("Input Error", "Phone should only contain numbers.")
        return False

    if len(phone.get()) < 10:  # Phone number length validation
        messagebox.showerror("Input Error", "Phone number should be at least 10 digits.")
        return False

    if not str(age.get()).isdigit():
        messagebox.showerror("Input Error", "Age should be a valid number.")
        return False

    return True


def search_item():
    """Search for contacts by first name."""
    search_term = search_var.get()
    if not search_term:
        messagebox.showerror("Search Error", "Please enter a search term.")
        return

    for row in tree.get_children():
        tree.delete(row)

    rows = run_query("SELECT * FROM contacts WHERE first_name LIKE %s", ('%' + search_term + '%',))
    if not rows:
        messagebox.showinfo("Search Results", "No contacts found with that name.")
    
    for row in rows:
        tree.insert("", "end", values=row)


def refresh_table():
    """Refresh the treeview after a search or modification."""
    populate_treeview()


# ===== Double Click Event Handler ===== #

def on_item_double_click(event):
    """Populate the input fields with the selected contact's data on double-click."""
    selected_item = tree.selection()
    if selected_item:
        values = tree.item(selected_item)["values"]
        first_name.set(values[0])  # First Name
        last_name.set(values[1])   # Last Name
        age.set(values[2])         # Age
        phone.set(values[3])       # Phone
        address.set(values[4])     # Address


# ===== Buttons ===== #

create_contact = Button(app, text="Create Contact", width=12, command=add_item)
create_contact.grid(row=10, column=0, padx=5, pady=10)

delete_contact = Button(app, text="Delete Contact", width=12, command=delete_item)
delete_contact.grid(row=10, column=1, padx=5, pady=10)

update_contact = Button(app, text="Update Contact", width=12, command=update_item)
update_contact.grid(row=10, column=2, padx=5, pady=10)

clear_input = Button(app, text="Clear Input Text", width=12, command=clear_text)
clear_input.grid(row=10, column=3, padx=5, pady=10)

refresh_button = Button(app, text="Refresh Table", width=12, command=refresh_table)
refresh_button.grid(row=11, column=0, columnspan=4, padx=5, pady=10)


# ===== App Setup and Start ===== #

# Window dimensions
app.geometry("900x550")

# Initialize DB and populate treeview
init_db()
populate_treeview()

# Bind double-click event to the Treeview
tree.bind("<Double-1>", on_item_double_click)

# Start the GUI app
app.mainloop()
