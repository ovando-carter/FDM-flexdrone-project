import sqlite3  # to connect to sqlite3
from datetime import datetime # to modify dates to the SQL standard

###################################################################################################################################################################################
# Connect to sqlite
###################################################################################################################################################################################

connection = sqlite3.connect("./templates/database/flexdrone.db")

'''
# connection.total_changes is the total number of database rows that have been changed by connection
print(connection.total_changes)
'''

# connection.cursor() returns a Cursor object. 
# Cursor objects allow us to send SQL statements 
# to a SQLite database using cursor.execute().
cursor = connection.cursor()

###################################################################################################################################################################################
# SQL commands
###################################################################################################################################################################################

# Drop tables

cursor.execute("DROP TABLE IF EXISTS User")
cursor.execute("DROP TABLE IF EXISTS Orders")
cursor.execute("DROP TABLE IF EXISTS Drone")
cursor.execute("DROP TABLE IF EXISTS Component")
cursor.execute("DROP TABLE IF EXISTS Drone_Component")

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS User 
                                            (user_id INTEGER PRIMARY KEY,
                                            email VARCHAR(255) NOT NULL,
                                            psw VARCHAR(255) NOT NULL,
                                            Date_of_Birth DATE NOT NULL,
                                            First_Name VARCHAR(255) NOT NULL,
                                            Last_Name VARCHAR(255) NOT NULL,
                                            addressline1 VARCHAR(255) NOT NULL,
                                            addressline2 VARCHAR(255),
                                            town VARCHAR(255),
                                            city VARCHAR(255) NOT NULL,
                                            country VARCHAR(255) NOT NULL,
                                            postcode VARCHAR(255) NOT NULL,
                                            number1 INT NOT NULL,
                                            number2 VARCHAR(14),
                                            occupation VARCHAR(255),
                                            flyerID VARCHAR(255),
                                            operatorID VARCHAR(255),
                                            NAAID VARCHAR(255))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Orders
                                            (order_id INTEGER PRIMARY KEY,
                                            user_id INT NOT NULL,
                                            drone_id INT NOT NULL,
                                            camera_component_id INT,
                                            landing_component_id INT,
                                            blade_component_id INT,
                                            total decimal(10,2) NOT NULL,
                                            deliver_pickup VARCHAR(7) NOT NULL,
                                            delivery_address_line_1 VARCHAR(255),
                                            delivery_address_line_2 VARCHAR(255),
                                            delivery_town VARCHAR(255),
                                            delivery_city VARCHAR(255),
                                            delivery_country VARCHAR(255),
                                            delivery_postcode VARCHAR(255),
                                            billing_address_line_1 VARCHAR(255) NOT NULL,
                                            billing_address_line_2 VARCHAR(255),
                                            billing_town VARCHAR(255),
                                            billing_city VARCHAR(255),
                                            billing_country VARCHAR(255) NOT NULL,
                                            billing_postcode VARCHAR(255) NOT NULL,
                                            purchase_date DATE NOT NULL,
                                            delivery_date DATE,
                                            order_status VARCHAR(16) NOT NULL,
                                            cardname varchar(255) not null,
										    cardnumber int not null,
										    expmonth INT not null,
    										expyear INT not null,
	    									cvv int not null,
				    						company_name varchar(255))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Drone
                                            (drone_id INTEGER PRIMARY KEY,
                                            drone_name VARCHAR(255) NOT NULL,
                                            model_number VARCHAR(255) NOT NULL,
                                            [description] VARCHAR(255),
                                            dimension_height decimal(10,2),
                                            dimension_Width decimal(10,2),
                                            dimension_length decimal(10,2),
                                            price decimal(10,2) NOT NULL,
                                            stock INT NOT NULL,
                                            model_link VARCHAR(255))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Component
                                            (component_id INTEGER PRIMARY KEY,
                                            component_name VARCHAR(255) NOT NULL,
                                            component_type  VARCHAR(255) NOT NULL,
                                            price decimal(10,2) NOT NULL,
                                            stock INT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Drone_Component 
                                            (drone_id INT NOT NULL,
                                            component_id INT NOT NULL)''')



# Save the changes to the database
connection.commit()