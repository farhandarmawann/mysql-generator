import mysql.connector, re

# Connect to the database
conn = mysql.connector.connect(
    host="localhost", # Your Hostname
    user="root", # Your MySQL Username
    password="", # Your MySQL Password 
    database="techsmart" # Your Database Name
)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create table
def create_table():
    table_name = input("Enter table name: ")
    column_count = int(input("Enter number of columns: "))
    
    columns = []
    primary_key = None
    foreign_keys = []
    for i in range(column_count):
        column_name = input(f"Enter name for column {i+1}: ")
        column_type = input(f"Enter data type for column {column_name} (e.g., VARCHAR(50)): ")
        is_primary_key = input(f"Is column {column_name} a primary key? (y/n): ").lower()
        if is_primary_key == 'y':
            primary_key = column_name
        columns.append(f"`{column_name}` {column_type} NOT NULL")

        foreign_key_input = input(f"Is column {column_name} a foreign key? (y/n): ")
        if foreign_key_input.lower() == 'y':
            referenced_table = input(f"Enter name of referenced table for column {column_name}: ")
            referenced_column = input(f"Enter name of column in table {referenced_table}: ")
            foreign_keys.append((column_name, referenced_table, referenced_column))
    
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
    create_table_query += ",\n".join(columns)
    if primary_key:
        create_table_query += f",\nPRIMARY KEY (`{primary_key}`)"
    if foreign_keys:
        foreign_key_queries = [f"FOREIGN KEY (`{fk[0]}`) REFERENCES `{fk[1]}`(`{fk[2]}`)" for fk in foreign_keys]
        create_table_query += ",\n" + ",\n".join(foreign_key_queries)
    create_table_query += "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"
    
    print("SQL Query:")
    print(create_table_query)  # Print SQL query
    cursor.execute(create_table_query)
    print("Table created successfully")


# Insert data into table
def insert_data():
    # Show list of tables
    list_tables()
    
    # Choose table
    table_name = input("Enter table name: ")
    
    # Get list of columns from the table
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]

    # Show list of columns
    print("List of columns in the table:")
    for i, column_name in enumerate(column_names, start=1):
        print(f"{i}. {column_name}")

    # Ask for input values for each column
    values = []
    for column_name in column_names:
        value = input(f"Enter value for column {column_name}: ")
        values.append(value)

    # Create SQL query string to insert data
    insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['%s']*len(values))})"

    # Execute SQL query
    print("SQL Query:")
    insert_query = insert_query.format(*values)
    print(insert_query)  # Print SQL query
    cursor.execute(insert_query, values)
    conn.commit()
    print("Data inserted successfully")


# Edit data in a table
def edit_data():
    # Show list of tables
    list_tables()

    # Choose table
    table_name = input("Enter table name: ")

    # Show structure and content of the selected table
    view_table(table_name)

    # Ask for the ID of the data to be edited
    record_id = input("Enter the ID of the data to be edited: ")

    # Get column structure from the table
    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]

    # Show list of columns
    print("List of columns in the table:")
    for i, column_name in enumerate(column_names, start=1):
        print(f"{i}. {column_name}")

    # Ask for new values for each column
    new_values = []
    for column_name in column_names:
        new_value = input(f"Enter new value for column {column_name}: ")
        new_values.append(new_value)

    # Create SQL query string to update data
    update_query = f"UPDATE {table_name} SET "
    update_query += ", ".join([f"{column_name} = %s" for column_name in column_names])
    update_query += " WHERE id = %s"

    # Execute SQL query
    print("SQL Query:")
    update_values = new_values + [record_id]
    print(update_query % tuple(update_values))  # Print SQL query
    cursor.execute(update_query, update_values)
    conn.commit()
    print("Data updated successfully")


# Delete data from a table
def delete_data():
    # Show list of tables
    list_tables()
    
    # Choose table
    table_name = input("Enter table name: ")

    # Show structure and content of the selected table
    view_table(table_name)

    # Ask for the ID of the data to be deleted
    record_id = input("Enter the ID of the data to be deleted: ")

    # Create SQL query to delete data
    delete_query = f"DELETE FROM {table_name} WHERE id = %s"

    # Execute SQL query
    print("SQL Query:")
    print(delete_query)  # Print SQL query
    cursor.execute(delete_query, (record_id,))
    conn.commit()
    print("Data deleted successfully")


# View data in a table
def view_table(table_name):
    # Get column structure from the table
    describe_query = f"DESCRIBE `{table_name}`"
    cursor.execute(describe_query)
    columns = cursor.fetchall()

    print(f"\nColumn structure of table {table_name}:")
    for column in columns:
        print(column[0], "-", column[1])

    # Get data from the table
    select_query = f"SELECT * FROM `{table_name}`"
    cursor.execute(select_query)
    records = cursor.fetchall()

    if records:
        print("\nTable content:")
        for record in records:
            print(record)
    else:
        print(f"Table {table_name} is empty")


# View contents of the database
def view_database():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        select_query = f"SELECT * FROM `{table_name}`"
        print("SQL Query:")
        print(select_query)  # Print SQL query
        cursor.execute(select_query)
        records = cursor.fetchall()
        if records:
            print(f"Table content {table_name}:")
            for record in records:
                print(record)
        else:
            print(f"Table {table_name} is empty")
        print()  # Add a blank line between each table


# Print list of tables in the database
def list_tables():
    show_tables_query = "SHOW TABLES"
    print("SQL Query:")
    print(show_tables_query)  # Print SQL query
    cursor.execute(show_tables_query)
    tables = cursor.fetchall()
    print("List of tables in the database:")
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table[0]}")


# Drop table from the database
def drop_table():
    # Show list of tables
    list_tables()
    
    # Choose table
    table_name = input("Enter the name of the table to be dropped: ")

    # Create SQL query to drop table
    drop_table_query = f"DROP TABLE IF EXISTS {table_name}"

    # Execute SQL query
    print("SQL Query:")
    print(drop_table_query)  # Print SQL query
    cursor.execute(drop_table_query)
    conn.commit()
    print("Table dropped successfully")


# Function to display relations present in the database
def show_relations():
    # Get list of tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Initialize dictionary to store relations
    relations = {}

    # Collect relation information from each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
        create_table_query = cursor.fetchone()[1]
        foreign_keys = re.findall(r"FOREIGN KEY \(`(.*?)`\) REFERENCES `(.*?)` \(`(.*?)`\)", create_table_query)
        if foreign_keys:
            relations[table_name] = [(fk[0], fk[1], fk[2]) for fk in foreign_keys]

    # Display relations present in the database
    print("Relations present in the database:")
    for table_name, foreign_keys in relations.items():
        print(f"Table '{table_name}' has relations with:")
        for fk in foreign_keys:
            print(f"- Column '{fk[0]}' references table '{fk[1]}' on column '{fk[2]}'")


# Menu options
def menu():
    print("=============== WELCOME TO MYSQL BUILDER ===============")
    print("Menu:")
    print("1. Add Table")
    print("2. Drop Table")
    print("3. Add Content")
    print("4. Update Content")
    print("5. Delete Content")
    print("6. View Table Content")
    print("7. View Database Content")
    print("8. List Tables")
    print("9. Show Relations")
    print("0. Exit")

# Main program
try:
    while True:
        menu()
        choice = input("Select menu: ")

        if choice == '1':
            create_table() # Add Table
        elif choice == '2':
            drop_table() # Drop Table
        elif choice == '3':
            insert_data() # Add Data
        elif choice == '4':
            edit_data() # Edit Data
        elif choice == '5':
            delete_data() # Delete Data
        elif choice == '6':
            list_tables()
            table_name = input("Enter table name: ")
            view_table(table_name) # View Table Content
        elif choice == '7':
            view_database() # View Database Content
        elif choice == '8':
            list_tables() # List Tables
        elif choice == '9':
            show_relations() 
        elif choice == '0':
            break
        else:
            print("Invalid choice.")

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    # Close cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Connection closed")
