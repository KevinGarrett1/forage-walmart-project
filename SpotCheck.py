import pandas as pd

# Load CSV files
shipping_data_0 = pd.read_csv('data/shipping_data_0.csv')
shipping_data_1 = pd.read_csv('data/shipping_data_1.csv')
shipping_data_2 = pd.read_csv('data/shipping_data_2.csv')

# Define the entry to match
product_id = 1  # This maps to 'product' name in shipping_data_0 via product table
quantity = 59
origin_warehouse = 'd5566b15-b071-4acf-8e8e-c98433083b2d'
destination_store = '50d33715-4c77-4dd9-8b9d-ff1ca372a2a2'

# Cross-reference with shipping_data_0.csv
matching_rows = shipping_data_0[
    (shipping_data_0['product_quantity'] == quantity) &
    (shipping_data_0['origin_warehouse'] == origin_warehouse) &
    (shipping_data_0['destination_store'] == destination_store)
]

# Display the matched rows
print("Matching rows in shipping_data_0.csv:")
print(matching_rows)
