import sqlite3
import pandas as pd

# Path to your Excel file
excel_file = './yield.csv'  # Replace with the actual file name

# Read the Excel file into a pandas DataFrame
df = pd.read_csv(excel_file)

# Connect to SQLite database
connection = sqlite3.connect('project.db')
cursor = connection.cursor()

# Create a table based on the DataFrame's columns
table_name = 'Crop'  # Replace with the desired table name
columns = ', '.join([f"{col} TEXT" for col in df.columns])  # Assuming all columns are TEXT
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
cursor.execute(create_table_query)


# Insert data into the table
for _, row in df.iterrows():
    placeholders = ', '.join(['?'] * len(row))
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
    cursor.execute(insert_query, tuple(row))

# Commit changes and close the connection
connection.commit()
connection.close() #Closing a connection is important else it will throw error.

