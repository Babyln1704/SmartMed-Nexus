import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine TEXT,
    dose TEXT,
    frequency TEXT,
    reminder_time TEXT
)
""")

cursor.execute("""
INSERT INTO medicines
(medicine, dose, frequency, reminder_time)
VALUES (?, ?, ?, ?)
""",
(
    "Paracetamol 500mg",
    "1 tablet after food",
    "Twice daily",
    "09:00"
))

conn.commit()

print("Medicine saved successfully!")

conn.close()