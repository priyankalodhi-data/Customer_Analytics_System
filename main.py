import sqlite3

# Create database 
conn = sqlite3.connect("customer_data.db")
cursor = conn.cursor()

print("Database connected successfully")
# Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
)
""")

# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")

conn.commit()
print("Tables created successfully")
# Insert customers
customers = [
    (1, "Rahul", "Delhi"),
    (2, "Priya", "Mumbai"),
    (3, "Amit", "Bangalore"),
    (4, "Neha", "Delhi")
]

cursor.executemany("INSERT OR IGNORE INTO customers VALUES (?, ?, ?)", customers)

# Insert orders
orders = [
    (1, 1, 5000, "2025-01-10"),
    (2, 1, 7000, "2025-02-12"),
    (3, 2, 3000, "2025-01-15"),
    (4, 3, 15000, "2025-03-01"),
    (5, 4, 8000, "2025-02-20"),
    (6, 4, 6000, "2025-03-05")
]


cursor.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?)", orders)

conn.commit()
print("Sample data inserted")

cursor.execute("SELECT SUM(amount) FROM orders")
total_revenue = cursor.fetchone()[0]
print("Total Revenue:", total_revenue)
cursor.execute("""
SELECT c.name, SUM(o.amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
""")

print("\nCustomer Spending:")
for row in cursor.fetchall():
    print(row)
    cursor.execute("""
SELECT c.name,
       SUM(o.amount) as total_spent,
       CASE
           WHEN SUM(o.amount) > 15000 THEN 'High Value'
           WHEN SUM(o.amount) BETWEEN 8000 AND 15000 THEN 'Medium Value'
           ELSE 'Low Value'
       END as segment
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
""")

print("\nCustomer Segmentation:")
for row in cursor.fetchall():
    print(row)
    conn.close()
    