import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE medicines
ADD COLUMN patient_id INTEGER
""")

conn.commit()
conn.close()

print("patient_id column added successfully")