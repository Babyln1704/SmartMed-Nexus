import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

# Ravi (patient id = 1)
cursor.execute("""
UPDATE medicines
SET patient_id=1
WHERE id IN (9,10)
""")

# Lakshmi (patient id = 2)
cursor.execute("""
UPDATE medicines
SET patient_id=2
WHERE id IN (11,12)
""")

# Suresh (patient id = 3)
cursor.execute("""
UPDATE medicines
SET patient_id=3
WHERE id IN (13,15)
""")

conn.commit()
conn.close()

print("Medicines assigned successfully")