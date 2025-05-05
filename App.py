import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",    
)

mycursor = db.cursor()

# Create the database if it doesn't exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS contactDB")

# Select the database
db.database = "contactDB"

# Create a table with the required columns
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        first_name VARCHAR(255) PRIMARY KEY,
        surname VARCHAR(255),
        contact_number VARCHAR(255),
        age INT,
        address TEXT
    )
""")
