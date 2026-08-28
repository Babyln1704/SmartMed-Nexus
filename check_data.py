import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, medicine, dose, frequency, reminder_time, patient_id
FROM medicines
""")

rows = cursor.fetchall()

print("\n===== Medicines Table =====\n")

for row in rows:
    print(row)

conn.close()