import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE medicines
ADD COLUMN taken TEXT DEFAULT 'Pending'
""")

conn.commit()
conn.close()

print("Taken column added!")