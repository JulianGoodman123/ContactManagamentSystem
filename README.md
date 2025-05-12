Contact Management System
A simple app to manage individual contacts, offering CRUD (Create, Read, Update, Delete) functionality along with search capabilities.

Overview
This is a basic contact management application built using Python with Tkinter for the graphical user interface (GUI) and MySQL for database management. The app allows users to store, search, update, and delete contact information, including first name, last name, age, phone number, and address.

Features
Add Contact: Add a new contact with first name, last name, age, phone number, and address.

Delete Contact: Remove a contact by selecting it from the table.

Update Contact: Edit the details of an existing contact.

Search Contacts: Search for contacts by their first name.

Refresh Table: Reload the contact table to reflect any changes made.

Clear Input: Clear all input fields.

Double-click Editing: Double-click on a contact in the table to auto-fill the input fields with the selected contact's details for editing.

Requirements
Python 3.x

Tkinter (usually included with Python)

MySQL Server

To install MySQL, follow the instructions provided on the MySQL website.

You will also need to install the mysql-connector package:

bash
Copy
Edit
pip install mysql-connector-python
Database Setup
The application uses MySQL to store contact information. When the application is first run, it will automatically initialize the database and create the required contactDB database and contacts table if they don't already exist.

sql
Copy
Edit
CREATE DATABASE IF NOT EXISTS contactDB;

CREATE TABLE IF NOT EXISTS contacts (
first_name VARCHAR(255),
last_name VARCHAR(255),
age INT,
phone VARCHAR(255) UNIQUE,
address TEXT,
PRIMARY KEY (phone)
);
Functionality
Add a Contact:
Fill in the fields for first name, last name, age, phone, and address. Click the Create Contact button, and the new contact will be added to the database and shown in the contact table.

Delete a Contact:
Select a contact from the table and click the Delete Contact button. The contact will be removed from the database, and the table will update.

Update a Contact:
Double-click a contact in the table to load its details into the input fields. Modify the details and click Update Contact to save the changes.

Search for Contacts:
Type a first name into the search field and click Search. The table will show only the contacts that match the search term.

Refresh the Table:
Click the Refresh Table button to reload the table and reflect any recent changes.

Clear Input Fields:
Click the Clear Input Text button to reset all input fields to empty.

How to Run
Ensure that MySQL is installed and running on your machine.

Run the script to launch the contact management application.

The database will be automatically set up when the application starts.

Use the buttons and features described above to manage your contacts.

Code Structure
Database Setup
The functions init_db() and run_query() handle initializing the database and running queries.

GUI Setup
The GUI is built with Tkinter. It includes input fields for entering contact information and a Treeview to display the contacts. The Treeview is populated with data from the database.

Core Functions

populate_treeview(): Loads contacts into the Treeview from the database.

add_item(): Adds a new contact to the database.

delete_item(): Deletes a selected contact from the database.

update_item(): Updates a selected contact's details.

clear_text(): Clears all input fields.

validate_inputs(): Validates the input fields to ensure they are filled out correctly.

search_item(): Searches for contacts by first name.

refresh_table(): Refreshes the contact list.

Event Handlers

on_item_double_click(): Double-click a contact in the table to populate the input fields with that contact's information for editing.

GitHub Repository
You can find the full source code for this application here on GitHub.
