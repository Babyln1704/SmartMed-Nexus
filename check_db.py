import sqlite3

conn = sqlite3.connect("medicine.db")

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

print(cursor.fetchall())

conn.close()