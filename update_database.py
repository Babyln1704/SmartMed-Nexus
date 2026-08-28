import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE patients ADD COLUMN phone TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE patients ADD COLUMN address TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE patients ADD COLUMN blood TEXT")
except:
    pass

conn.commit()
conn.close()

print("Database Updated Successfully")