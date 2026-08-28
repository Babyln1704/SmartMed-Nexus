import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

cursor.execute("SELECT medicine FROM medicines")
data = cursor.fetchall()

conn.close()

medicines = [row[0] for row in data]

counts = {}

for med in medicines:
    counts[med] = counts.get(med, 0) + 1

plt.bar(counts.keys(), counts.values())

plt.title("Medicine Usage Statistics")
plt.xlabel("Medicine")
plt.ylabel("Count")

plt.xticks(rotation=45)

plt.show()