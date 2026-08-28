import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE users ADD COLUMN fullname TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
cursor.execute("ALTER TABLE users ADD COLUMN emergency_contact TEXT")

conn.commit()
conn.close()

print("Database Updated Successfully!")