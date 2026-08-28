import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(patients)")

for row in cursor.fetchall():
    print(row)

conn.close()