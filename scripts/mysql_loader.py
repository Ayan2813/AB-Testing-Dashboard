import mysql.connector
import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
csv_file = os.path.join(DATA_DIR, 'experiment_data.csv')

# Read CSV
df = pd.read_csv(csv_file)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # your MySQL username
    password="",  # your MySQL password
    database="ab_testing_db"
)
cursor = conn.cursor()
cursor.execute("TRUNCATE TABLE experiment_data;")
# Insert data into MySQL
for i, row in df.iterrows():
    cursor.execute("""
        INSERT INTO experiment_data (user_id, group_name, converted, device, country, traffic_source, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("CSV data loaded into MySQL successfully!")
