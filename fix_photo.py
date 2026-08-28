import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE patients
SET photo='ravi_pic.jpg'
WHERE id=12
""")

conn.commit()
conn.close()

print("Updated")