import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE patients
SET caregiver_username='baby'
""")

conn.commit()
conn.close()

print("Patients Updated Successfully")