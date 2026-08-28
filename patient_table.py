import sqlite3

conn = sqlite3.connect("medicine.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    caregiver_username TEXT,

    patient_name TEXT,

    age INTEGER,

    photo TEXT

)
""")

conn.commit()

conn.close()

print("Patients table created successfully!")