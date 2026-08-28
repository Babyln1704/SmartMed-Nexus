import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM reminders")

rows = cursor.fetchall()

print("\n========== REMINDERS TABLE ==========\n")

if not rows:
    print("No reminders found!")

for row in rows:
    print(row)

conn.close()