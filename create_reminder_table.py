import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id INTEGER NOT NULL,

    medicine TEXT,

    reminder_type TEXT NOT NULL,

    reminder_time TEXT NOT NULL,

    meal TEXT,

    dose TEXT,

    instruction TEXT,

    voice_text TEXT,

    notification_text TEXT,

    priority TEXT,

    status TEXT DEFAULT 'Pending',

    FOREIGN KEY(patient_id)
    REFERENCES patients(id)

)
""")

conn.commit()

print("✅ Reminders table created successfully!")

conn.close()