import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM patients")

conn.commit()
conn.close()

print("All patients deleted")