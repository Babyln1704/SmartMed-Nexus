import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, patient_name, photo
FROM patients
""")

for row in cursor.fetchall():
    print(row)

conn.close()