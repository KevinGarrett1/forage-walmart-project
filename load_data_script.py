import os
import pandas as pd
import sqlite3

# Paths to the CSV files
data_0_path = 'C:/Users/black/forage-walmart-task-4/data/shipping_data_0.csv'
data_1_path = 'C:/Users/black/forage-walmart-task-4/data/shipping_data_1.csv'
data_2_path = 'C:/Users/black/forage-walmart-task-4/data/shipping_data_2.csv'

# Verify that each file exists before loading
for path in [data_0_path, data_1_path, data_2_path]:
    if not os.path.exists(path):
        print(f"Error: File not found at path: {path}")
        exit(1)

# Load data from CSV files
data_0 = pd.read_csv(data_0_path)
data_1 = pd.read_csv(data_1_path)
data_2 = pd.read_csv(data_2_path)

# Connect to SQLite database
conn = sqlite3.connect('shipment_database.db')
cursor = conn.cursor()

# Insert data from data_0 (assuming id and name) into a 'product' table
for _, row in data_0.iterrows():
    # Cast to ensure integer for 'id' and string for 'name'
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO product (id, name)
            VALUES (?, ?)
        ''', (
            int(row['driver_identifier']),  # Convert to integer
            str(row['product'])              # Ensure name is a string
        ))
    except ValueError as e:
        print(f"Data type error on row {row}: {e}")

# Merge data_1 and data_2 on 'shipment_identifier' and insert into 'shipment' table
merged_data = pd.merge(data_1, data_2, on='shipment_identifier', how='inner')

for _, row in merged_data.iterrows():
    # Insert into shipment table using the correct fields with explicit type conversions
    try:
        cursor.execute('''
            INSERT INTO shipment (id, product, quantity, origin, destination, driver)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            int(row['shipment_identifier']),     # Convert to integer
            str(row['product']),                  # Ensure product is a string
            int(row['on_time']),                  # Convert quantity to integer
            str(row['origin_warehouse']),         # Ensure origin is a string
            str(row['destination_store']),        # Ensure destination is a string
            str(row['driver_identifier'])         # Ensure driver is a string
        ))
    except ValueError as e:
        print(f"Data type error on row {row}: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()
