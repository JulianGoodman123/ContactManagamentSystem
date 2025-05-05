# Imports list for application
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root", 
    database="contactDB",   
)

mycursor = db.cursor()

# Create the database if it doesn't exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS contactDB")

# Select the database
db.database = "contactDB"

# Create a table with the required columns (again only if the database doesn't exist)
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        full_name VARCHAR(255) PRIMARY KEY,
        age INT,
        contact_number VARCHAR(255),
        address TEXT
    )
""")

