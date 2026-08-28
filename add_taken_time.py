import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE medicines
ADD COLUMN taken_time TEXT
""")

conn.commit()
conn.close()

print("taken_time column added!")