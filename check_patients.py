import sqlite3

conn = sqlite3.connect("medicine.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM patients")

print(cursor.fetchall())

conn.close()