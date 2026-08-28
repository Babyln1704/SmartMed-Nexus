import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO patients
(caregiver_username, patient_name, age, photo)
VALUES
('admin', 'Ravi Kumar', 70, 'ravi.jpg')
""")

cursor.execute("""
INSERT INTO patients
(caregiver_username, patient_name, age, photo)
VALUES
('admin', 'Lakshmi Devi', 65, 'lakshmi.jpg')
""")

cursor.execute("""
INSERT INTO patients
(caregiver_username, patient_name, age, photo)
VALUES
('admin', 'Suresh Kumar', 72, 'suresh.jpg')
""")

conn.commit()
conn.close()

print("Patients Added Successfully")