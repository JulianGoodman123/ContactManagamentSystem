import mysql.connector

# Connect to the MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

# Create a cursor object to communicate with the database 
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

