import sqlite3

conn = sqlite3.connect("medicine.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(medicines)")

print(cursor.fetchall())

conn.close()