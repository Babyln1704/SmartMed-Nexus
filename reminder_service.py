import sqlite3


# ==========================================
# DELETE OLD REMINDERS
# ==========================================

def delete_patient_reminders(patient_id):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM reminders

        WHERE patient_id = ?

    """, (patient_id,))

    conn.commit()
    conn.close()


# ==========================================
# SAVE REMINDERS
# ==========================================

def save_reminders(patient_id, reminder_groups):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    # Remove old reminders
    delete_patient_reminders(patient_id)

    for reminders in reminder_groups:

        for reminder in reminders:

            cursor.execute("""

            INSERT INTO reminders
            (

                patient_id,

                medicine,

                reminder_type,

                reminder_time,

                meal,

                dose,

                instruction,

                voice_text,

                notification_text,

                priority,

                status

            )

            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )

            """,

            (

                patient_id,

                reminder.get("medicine"),

                reminder["type"],

                reminder["time"],

                reminder.get("meal"),

                reminder.get("dose"),

                reminder.get("instruction"),

                reminder.get("voice_text"),

                reminder.get("notification_text"),

                reminder.get("priority"),

                reminder.get("status", "Pending")

            ))

    conn.commit()
    conn.close()


# ==========================================
# GET PATIENT REMINDERS
# ==========================================

def get_patient_reminders(patient_id):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            *

        FROM reminders

        WHERE patient_id = ?

        ORDER BY reminder_time

    """, (patient_id,))

    reminders = cursor.fetchall()

    conn.close()

    return reminders