import os
import mysql.connector
from mysql.connector import Error

from apis.models import employees, invoices, rates, BaseCurrency, sales, suppliers, ordersandproducts, returnedproducts, \
    orders, products, Poisonous, categories, traillogs

# Define your MySQL credentials
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306

# Define the database name
DATABASE_NAME = 'retail_db'


# Function to create the database and tables
def create_database_and_tables():
    try:
        # Connect to MySQL Server
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Check if the database already exists
        cursor.execute(f"SHOW DATABASES LIKE '{DATABASE_NAME}'")
        database_exists = cursor.fetchone()

        if not database_exists:
            # Create the database
            cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
            print(f"Database '{DATABASE_NAME}' created successfully")

        # Switch to the specified database
        cursor.execute(f"USE {DATABASE_NAME}")

        # Iterate through the models and create tables
        for model in [
            employees, invoices, rates, BaseCurrency, sales, suppliers,
            categories, products, orders, returnedproducts, ordersandproducts,
            traillogs, Poisonous,
        ]:
            table_name = model._meta.db_table
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

            # Iterate through model fields and add them to the query
            for field in model._meta.fields:
                field_name = field.name
                field_type = field.db_type(connection)

                query += f"{field_name} {field_type}, "

            query = query[:-2] + ")"
            cursor.execute(query)
            print(f"Table '{table_name}' created successfully")

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed")


if __name__ == "__main__":
    # Check if the MySQL Server directory exists
    mysql_installation_path = r"C:\Program Files\MySQL\MySQL Server 8.0"

    if os.path.exists(mysql_installation_path):
        print(f"MySQL Server found at {mysql_installation_path}.")
        os.chdir(mysql_installation_path)
        create_database_and_tables()
    else:
        print(f"MySQL Server not found at {mysql_installation_path}. Please update the path.")
