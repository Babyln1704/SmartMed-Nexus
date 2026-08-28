"""
=========================================
SmartMed AI
Interaction Service
=========================================

This module connects

OCR
↓

Medicine Extraction

↓

Existing Patient Medicines

↓

Drug Interaction Analysis

↓

AI Reminder Suggestions
"""

import sqlite3



from medicine_extractor_v2 import (
    extract_medicines_v2,
    build_prescription_information
)

#from medicine_extractor import extract_medicines
from check import (check_prescription_interactions_ai, check_existing_vs_new)


# ==========================================
# GET EXISTING MEDICINES
# ==========================================

def get_existing_medicines(patient_id):
    """
    Return all medicines assigned
    to one patient.
    """

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT medicine
        FROM medicines
        WHERE patient_id = ?
    """, (patient_id,))

    rows = cursor.fetchall()

    conn.close()

    medicines = []

    for row in rows:

        if row[0]:
            medicines.append(row[0])

    return medicines

# ==========================================
# MERGE MEDICINES
# ==========================================

def merge_medicines(existing, new):
    """
    Merge medicine lists and
    remove duplicates.
    """

    combined = []

    for medicine in existing:

        if medicine not in combined:
            combined.append(medicine)

    for medicine in new:

        if medicine not in combined:
            combined.append(medicine)

    return combined

# ==========================================
# AI REMINDER SCHEDULER
# ==========================================

def generate_ai_schedule(interaction_report):
    """
    Generates reminder suggestions based on
    interaction severity.

    This function NEVER changes the doctor's
    prescription. It only suggests reminder spacing.
    """

    schedule = {
        "has_suggestion": False,
        "recommended_gap": 0,
        "message": "No reminder adjustment required.",
        "adjustments": []
    }

    interactions = interaction_report.get("interactions", [])

    if not interactions:
        return schedule

    highest = "LOW"

    severity_order = {
        "LOW": 1,
        "MODERATE": 2,
        "HIGH": 3
    }

    adjustments = []

    # ------------------------------------
    # Find highest severity
    # ------------------------------------

    for interaction in interactions:

        pair = interaction["pair_display"].split(" + ")

        existing = pair[0].strip()
        new = pair[1].strip()

        for risk in interaction["risks"]:

            severity = risk["severity"].upper()

            if severity_order.get(severity, 0) > severity_order.get(highest, 0):
                highest = severity

    # ------------------------------------
    # Decide reminder gap
    # ------------------------------------

    gap = 0
    message = ""

    if highest == "LOW":

        gap = 15

        message = (
            "Potential interaction detected. "
            "Suggested reminder gap: 15 minutes."
        )

    elif highest == "MODERATE":

        gap = 30

        message = (
            "Moderate interaction detected. "
            "Suggested reminder gap: 30 minutes."
        )

    elif highest == "HIGH":

        gap = 60

        message = (
            "High interaction detected. "
            "Suggested reminder gap: 60 minutes."
        )

    # ------------------------------------
    # Build schedule
    # ------------------------------------

    if gap > 0:

        schedule["has_suggestion"] = True
        schedule["recommended_gap"] = gap
        schedule["message"] = message

        for interaction in interactions:

            pair = interaction["pair_display"].split(" + ")

            adjustments.append({

                "existing": pair[0].strip(),

                "new": pair[1].strip(),

                "gap": gap

            })

    schedule["adjustments"] = adjustments

    return schedule

# ==========================================
# ANALYZE PRESCRIPTION
# ==========================================

def analyze_prescription(patient_id, ocr_text, lang="en"):
    """
    Complete SmartMed AI Pipeline.
    """

    # Step 1
    # ==========================================
# Step 1
# SmartMed AI Medicine Extraction V2
# ==========================================

    detected_medicines = extract_medicines_v2(ocr_text)

    parsed_medicines = build_prescription_information(
       ocr_text,
       detected_medicines
)
    

# Medicine names only
# (used for interaction checking)

    new_medicines = [

    medicine["medicine"]

    for medicine in parsed_medicines

]
    
    print("\n========== OCR ==========")
    print(ocr_text)

    print("\n========== DETECTED ==========")
    print(detected_medicines)

    print("\n========== PARSED ==========")
    for med in parsed_medicines:
     print(med)

    print("\n========== NEW MEDICINES ==========")
    print(new_medicines)
    #new_medicines = extract_medicines(ocr_text)

    # Step 2
    existing_medicines = get_existing_medicines(patient_id)
    all_existing = True

    for medicine in new_medicines:

        if medicine.lower() not in [

             m.lower()

             for m in existing_medicines

    ]:

             all_existing = False
             break
    print("Existing Medicines:", existing_medicines)

    # Step 3
    combined_medicines = merge_medicines(
        existing_medicines,
        new_medicines
    )

    # Step 4
    interaction_report = check_existing_vs_new(
        existing_medicines,
        new_medicines,
        lang
    )

    ai_schedule = generate_ai_schedule(
    interaction_report
)
    if all_existing and new_medicines:

      return {

        "duplicate_prescription": True,

        "message": "Prescription already uploaded.",

        "new_medicines": [],

        "parsed_medicines": [],

        "existing_medicines": existing_medicines,

        "combined_medicines": existing_medicines,

        "interaction_report": None,

        "ai_schedule": None

    }
   
    

    # Step 5
    result = {

        "new_medicines": new_medicines,

        "parsed_medicines": parsed_medicines,

        "existing_medicines": existing_medicines,

        "combined_medicines": combined_medicines,

        "interaction_report": interaction_report,

        "ai_schedule": ai_schedule
    
    }
    return result


# ==========================================
# SAVE NEW MEDICINES
# ==========================================
def save_medicines(patient_id, medicines,ai_schedule=None):
    """
    Save medicines into database.

    Supports BOTH formats:

    1.
    [
        "dolo 650",
        "pan 40"
    ]

    2.
    [
        {
            "medicine":"dolo 650",
            "generic":"acetaminophen",
            "strength":"650",
            "dose":"1 tablet",
            "frequency":"Twice Daily",
            "duration":"3 Days",
            "instruction":"After Food",
            "source":"Indian Brand",
            "confidence":100.0
        }
    ]
    """

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    # ------------------------------------

    for item in medicines:

        # ------------------------------------
        # OLD FORMAT
        # ------------------------------------

        if isinstance(item, str):

            medicine = item
            generic = ""
            strength = ""
            dose = "Not Specified"
            frequency = "Not Specified"
            duration = "Not Found"
            instruction = "Not Found"
            source = ""
            confidence = 0

        # ------------------------------------
        # NEW FORMAT
        # ------------------------------------

        else:

            medicine = item.get("medicine", "")
            generic = item.get("generic", "")
            strength = item.get("strength", "")
            dose = item.get("dose", "Not Specified")
            frequency = item.get("frequency", "Not Specified")
            duration = item.get("duration", "Not Found")
            instruction = item.get("instruction", "Not Found")
            source = item.get("source", "")
            confidence = item.get("confidence", 0)

        # ------------------------------------
        # Reminder Time
        # ------------------------------------

        frequency_lower = frequency.lower()

        if "once" in frequency_lower:
            if instruction == "Before Food":

             reminder_time = "09:00"
            elif instruction == "After Food":
               reminder_time = "10:00"

            elif instruction == "At Bedtime":
               reminder_time = "22:00"

            else:
               reminder_time = "09:00" 

        elif "twice" in frequency_lower:

            if instruction == "Before Food":
                reminder_time = "09:00,20:00"

            elif instruction == "After Food":
               reminder_time = "10:00,21:00"

            else:
              reminder_time = "09:00,21:00"

        elif "three" in frequency_lower:

            if instruction == "Before Food":
              reminder_time = "09:00,13:00,20:00"

            elif instruction == "After Food":
              reminder_time = "10:00,14:00,21:00"

            else:
              reminder_time = "08:00,14:00,20:00"

        else:

            reminder_time = "09:00"
        
       

        # ------------------------------------
        # Skip duplicate medicine
        # ------------------------------------

        cursor.execute("""

            SELECT id

            FROM medicines

            WHERE patient_id = ?

            AND LOWER(medicine)=LOWER(?)

        """, (patient_id, medicine))

        if cursor.fetchone():

            continue

        # ------------------------------------
        # Save
        # ------------------------------------

        cursor.execute("""

        INSERT INTO medicines
        (
            medicine,
            dose,
            frequency,
            reminder_time,
            taken,
            taken_time,
            patient_id,
            generic,
            strength,
            duration,
            instruction,
            source,
            confidence
        )

        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )

        """,

        (

            medicine,
            dose,
            frequency,
            reminder_time,
            "Pending",
            None,
            patient_id,
            generic,
            strength,
            duration,
            instruction,
            source,
            confidence

        ))

    conn.commit()
    conn.close()

def update_dashboard_reminder_times(
    patient_id,
    reminder_groups
):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    medicine_times = {}

    # Collect all reminder times
    for reminders in reminder_groups:

        for reminder in reminders:

            if reminder["type"] != "Medicine":
                continue

            medicine = reminder["medicine"]

            if medicine not in medicine_times:
                medicine_times[medicine] = []

            medicine_times[medicine].append(
                reminder["time"]
            )

    # Update medicines table
    for medicine, times in medicine_times.items():

        reminder_time = ",".join(times)

        cursor.execute("""

            UPDATE medicines

            SET reminder_time=?

            WHERE patient_id=?
            AND LOWER(medicine)=LOWER(?)

        """, (

            reminder_time,

            patient_id,

            medicine

        ))

    conn.commit()
    conn.close()


def get_patient_medicines(patient_id):

    """
    Returns all medicines of a patient
    in the same format required by
    generate_reminder_times().
    """

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            medicine,
            dose,
            frequency,
            duration,
            instruction

        FROM medicines

        WHERE patient_id=?

    """, (patient_id,))

    rows = cursor.fetchall()

    conn.close()

    medicines = []

    for row in rows:

        medicines.append({

            "medicine": row[0],

            "dose": row[1],

            "frequency": row[2],

            "duration": row[3],

            "instruction": row[4]

        })

    return medicines

'''def save_medicines(
    patient_id,
    medicines,
    dose="Not Specified",
    frequency="Not Specified",
    reminder_time="09:00"
):
    """
    Save only NEW medicines for the patient.
    Existing medicines are ignored.
    """

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    for medicine in medicines:

        # Check whether medicine already exists
        cursor.execute("""
            SELECT id
            FROM medicines
            WHERE
                patient_id = ?
            AND
                LOWER(medicine) = LOWER(?)
        """, (patient_id, medicine))

        exists = cursor.fetchone()

        if exists:
            continue

        cursor.execute("""
            INSERT INTO medicines
            (
                medicine,
                dose,
                frequency,
                reminder_time,
                patient_id
            )
            VALUES
            (
                ?, ?, ?, ?, ?
            )
        """, (
            medicine,
            dose,
            frequency,
            reminder_time,
            patient_id
        ))

    conn.commit()
    conn.close()'''




if __name__ == "__main__":

    sample_text = """

    Tab Dolo650

    Glycomet500

    Ecosprln75

    """

    result = analyze_prescription(
        patient_id=1,
        ocr_text=sample_text
    )

    print("\n========== AI Schedule ==========\n")

    print(result["ai_schedule"])