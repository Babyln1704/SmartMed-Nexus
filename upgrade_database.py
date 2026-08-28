import sqlite3

conn = sqlite3.connect("medicine.db")
cursor = conn.cursor()

print("Upgrading medicines table...\n")


def add_column(column_name, column_type):

    try:
        cursor.execute(
            f"ALTER TABLE medicines ADD COLUMN {column_name} {column_type}"
        )
        print(f"✓ Added column : {column_name}")

    except sqlite3.OperationalError:

        # Column already exists
        print(f"• Already exists : {column_name}")


# ======================================
# AI Medicine Information
# ======================================

add_column("generic", "TEXT")

add_column("strength", "TEXT")

add_column("duration", "TEXT")

add_column("instruction", "TEXT")

add_column("source", "TEXT")

add_column("confidence", "REAL")

conn.commit()

print("\nDatabase upgraded successfully!")

conn.close()