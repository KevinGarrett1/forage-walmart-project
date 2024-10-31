import sqlite3
import pandas as pd

# Load CSV files with the correct path for the data subdirectory
shipping_data_0 = pd.read_csv('data/shipping_data_0.csv')
shipping_data_1 = pd.read_csv('data/shipping_data_1.csv')
shipping_data_2 = pd.read_csv('data/shipping_data_2.csv')

# Connect to the SQLite database
conn = sqlite3.connect('shipment_database.db')
cursor = conn.cursor()

# Step 1: Populate the product table with unique products from shipping_data_0
unique_products = shipping_data_0['product'].unique()
for product in unique_products:
    cursor.execute("INSERT OR IGNORE INTO product (name) VALUES (?)", (product,))

# Step 2: Map products to their IDs for shipment table insertion
cursor.execute("SELECT id, name FROM product")
product_map = {name: prod_id for prod_id, name in cursor.fetchall()}

# Step 3: Populate the shipment table using shipping_data_0
for index, row in shipping_data_0.iterrows():
    product_id = product_map.get(row['product'])
    origin = row['origin_warehouse']
    destination = row['destination_store']
    quantity = row['product_quantity']
    
    # Insert shipment details into the shipment table
    cursor.execute("""
        INSERT INTO shipment (product_id, quantity, origin, destination)
        VALUES (?, ?, ?, ?)
    """, (product_id, quantity, origin, destination))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data population complete.")
