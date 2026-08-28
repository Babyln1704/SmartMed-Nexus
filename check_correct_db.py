import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(medicines)")

columns = cursor.fetchall()

print("\nCurrent Medicines Table\n")

for column in columns:
    print(column)

conn.close()