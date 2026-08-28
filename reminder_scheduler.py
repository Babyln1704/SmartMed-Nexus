"""
=========================================
SmartMed AI
Reminder Scheduler V1
=========================================
"""

from datetime import datetime, timedelta


# =========================================
# DEFAULT SETTINGS
# =========================================

DEFAULT_SETTINGS = {

    # Default Meal Times
    "breakfast": "09:30",
    "lunch": "13:30",
    "dinner": "20:30",

    # Time Gap
    "before_food_gap": 30,
    "after_food_gap": 30,

    # Drug Interaction Gap
    "interaction_gap": 30,

    # Default Time (No Food Instruction)
    "default_once_daily": "09:00",

    # Voice Language
    "voice_language": "en"

}


# =========================================
# TIME UTILITIES
# =========================================

def add_minutes(time_string, minutes):

    t = datetime.strptime(time_string, "%H:%M")

    t = t + timedelta(minutes=minutes)

    return t.strftime("%H:%M")


def subtract_minutes(time_string, minutes):

    return add_minutes(
        time_string,
        -minutes
    )


# =========================================
# GET MEAL TIMES
# =========================================

def get_meal_times():

    return {

        "Breakfast": DEFAULT_SETTINGS["breakfast"],

        "Lunch": DEFAULT_SETTINGS["lunch"],

        "Dinner": DEFAULT_SETTINGS["dinner"]

    }



    
# =========================================
# CALCULATE MEDICINE TIMES
# =========================================

def calculate_medicine_times(
    frequency,
    instruction,
    interaction_gap=0
):

    meals = get_meal_times()

    medicine_times = []

    # ------------------------------------
    # Once Daily
    # ------------------------------------

    if frequency == "Once Daily":

        meal_time = meals["Breakfast"]

        if instruction == "After Food":

            medicine_time = add_minutes(
                meal_time,
                DEFAULT_SETTINGS["after_food_gap"]
            )

        elif instruction == "Before Food":

            medicine_time = subtract_minutes(
                meal_time,
                DEFAULT_SETTINGS["before_food_gap"]
            )

        else:

            medicine_time = DEFAULT_SETTINGS[
                "default_once_daily"
            ]

        medicine_times.append(medicine_time)

    # ------------------------------------
    # Twice Daily
    # ------------------------------------

    elif frequency == "Twice Daily":

        selected = [

            meals["Breakfast"],

            meals["Dinner"]

        ]

        for meal_time in selected:

            if instruction == "After Food":

                medicine_times.append(

                    add_minutes(
                        meal_time,
                        DEFAULT_SETTINGS["after_food_gap"]
                    )

                )

            elif instruction == "Before Food":

                medicine_times.append(

                    subtract_minutes(
                        meal_time,
                        DEFAULT_SETTINGS["before_food_gap"]
                    )

                )

            else:

                medicine_times.append(meal_time)

    # ------------------------------------
    # Three Times Daily
    # ------------------------------------

    elif frequency == "Three Times Daily":

        selected = [

            meals["Breakfast"],

            meals["Lunch"],

            meals["Dinner"]

        ]

        for meal_time in selected:

            if instruction == "After Food":

                medicine_times.append(

                    add_minutes(
                        meal_time,
                        DEFAULT_SETTINGS["after_food_gap"]
                    )

                )

            elif instruction == "Before Food":

                medicine_times.append(

                    subtract_minutes(
                        meal_time,
                        DEFAULT_SETTINGS["before_food_gap"]
                    )

                )

            else:

                medicine_times.append(meal_time)

    # ------------------------------------
    # Four Times Daily
    # ------------------------------------

    elif frequency == "Four Times Daily":

        medicine_times = [

            "06:00",

            "12:00",

            "18:00",

            "22:00"

        ]

    # ------------------------------------
    # Interaction Gap
    # ------------------------------------

    if interaction_gap > 0:

        adjusted = []

        previous = None

        for time in medicine_times:

            if previous is None:

                adjusted.append(time)

                previous = time

            else:

                new_time = add_minutes(
                    previous,
                    interaction_gap
                )

                adjusted.append(new_time)

                previous = new_time

        medicine_times = adjusted

    return medicine_times  


# =========================================
# BUILD REMINDER OBJECTS
# =========================================

def build_reminders(

    medicine,

    interaction_gap=0

):

    reminders = []

    times = calculate_medicine_times(

        medicine["frequency"],

        medicine["instruction"],

        interaction_gap

    )

    

    # ------------------------------------
    # Create Meal Reminders ONLY
    # when food instruction exists
    # ------------------------------------

       # ------------------------------------
    # Medicine Reminders
    # ------------------------------------

    for reminder_time in times:

        dose = medicine.get(

            "dose",

            ""

        )

        instruction = medicine.get(

            "instruction",

            ""

        )

        if dose != "Not Found" and dose:

            voice = (

                f"It is time to take "

                f"{dose} of "

                f"{medicine['medicine']} "

                f"{instruction.lower()}."

            )

        else:

            voice = (

                f"It is time to take "

                f"{medicine['medicine']}."

            )

        reminders.append({

            "time":

            reminder_time,

            "type":

            "Medicine",

            "medicine":

            medicine["medicine"],

            "dose":

            dose,

            "instruction":

            instruction,

            "voice_text":

            voice,

            "notification_text":

            f"Take {medicine['medicine']}.",

            "priority":

            "Normal",

            "status":

            "Pending"

        })

    reminders.sort(

        key=lambda x: x["time"]

    )

    return reminders


# =========================================
# ADJUST INTERACTION GAP BETWEEN MEDICINES
# =========================================

'''def adjust_interaction_gap_between_medicines(
    reminder_groups,
    gap_minutes
):
    """
    Adjust reminder times between different medicines.

    reminder_groups:
    [
        build_reminders(medicine1),
        build_reminders(medicine2),
        ...
    ]

    Returns updated reminder groups.
    """

    if gap_minutes <= 0:
        return reminder_groups

    previous_medicine_time = None

    for reminders in reminder_groups:

        # Find only medicine reminders
        medicine_indexes = [

            i

            for i, r in enumerate(reminders)

            if r["type"] == "Medicine"

        ]

        if not medicine_indexes:
            continue

        first_index = medicine_indexes[0]

        first_time = reminders[first_index]["time"]

        # -----------------------------
        # First medicine
        # -----------------------------

        if previous_medicine_time is None:

            previous_medicine_time = first_time
            continue

        # -----------------------------
        # Calculate shift
        # -----------------------------

        target_time = add_minutes(
            previous_medicine_time,
            gap_minutes
        )

        offset = (

            datetime.strptime(
                target_time,
                "%H:%M"
            )

            -

            datetime.strptime(
                first_time,
                "%H:%M"
            )

        )

        # -----------------------------
        # Shift ALL medicine reminders
        # -----------------------------

        for index in medicine_indexes:

            old = reminders[index]["time"]

            new = (

                datetime.strptime(
                    old,
                    "%H:%M"
                )

                + offset

            ).strftime("%H:%M")

            reminders[index]["time"] = new

        previous_medicine_time = reminders[first_index]["time"]

    return reminder_groups'''

from datetime import datetime, timedelta


def adjust_interaction_gap_pairwise(
    reminder_groups,
    ai_schedule
):
    """
    SmartMed AI Scheduler

    Rules
    -----
    1. Move ONLY the new medicine.
    2. Existing medicines never move.
    3. Meal reminders never move.
    4. Different instructions -> No movement.
    5. Only interaction pairs are adjusted.
    """

    adjustments = ai_schedule.get("adjustments", [])

    if not adjustments:
        return reminder_groups

    for adjustment in adjustments:

        existing_name = adjustment["existing"].lower().strip()
        new_name = adjustment["new"].lower().strip()
        gap = adjustment["gap"]

        existing_reminder = None
        new_reminder = None

        # ------------------------------------
        # Find reminders
        # ------------------------------------

        for reminders in reminder_groups:

            for reminder in reminders:

                if reminder["type"] != "Medicine":
                    continue

                medicine = reminder["medicine"].lower().strip()

                if medicine == existing_name:
                    existing_reminder = reminder

                elif medicine == new_name:
                    new_reminder = reminder

        if existing_reminder is None or new_reminder is None:
            continue

        # ------------------------------------
        # Check food instruction
        # ------------------------------------

        existing_instruction = existing_reminder.get(
            "instruction",
            ""
        )

        new_instruction = new_reminder.get(
            "instruction",
            ""
        )

        if existing_instruction != new_instruction:
            continue

        # ------------------------------------
        # Calculate new time
        # ------------------------------------

        existing_time = datetime.strptime(
            existing_reminder["time"],
            "%H:%M"
        )

        target_time = (
            existing_time +
            timedelta(minutes=gap)
        ).strftime("%H:%M")

        # ------------------------------------
        # Move ONLY the new medicine
        # ------------------------------------

        for reminders in reminder_groups:

            for reminder in reminders:

                if reminder["type"] != "Medicine":
                    continue

                if reminder["medicine"].lower().strip() != new_name:
                    continue

                old_time = datetime.strptime(
                    reminder["time"],
                    "%H:%M"
                )

                first_time = datetime.strptime(
                    new_reminder["time"],
                    "%H:%M"
                )

                offset = old_time - first_time

                reminder["time"] = (
                    datetime.strptime(
                        target_time,
                        "%H:%M"
                    ) + offset
                ).strftime("%H:%M")

    return reminder_groups





def generate_reminder_times(
        medicines,
        ai_schedule=None):
    """
    Build reminder objects for all medicines.
    Generate meal reminders only once.
    Apply AI interaction gap if required.
    """

    reminder_groups = []

    # ------------------------------------
    # Build medicine reminders
    # ------------------------------------

    for medicine in medicines:

        reminder_groups.append(

            build_reminders(
                medicine
            )

        )

    # ------------------------------------
    # Generate Meal Reminders ONLY ONCE
    # ------------------------------------

    meal_times = get_meal_times()

    meal_set = set()

    meal_reminders = []

    for medicine in medicines:

        instruction = medicine.get(
            "instruction",
            ""
        )

        frequency = medicine.get(
            "frequency",
            ""
        )

        if instruction not in [

            "Before Food",

            "After Food"

        ]:
            continue

        if frequency == "Once Daily":

            meals = [

                "Breakfast"

            ]

        elif frequency == "Twice Daily":

            meals = [

                "Breakfast",

                "Dinner"

            ]

        elif frequency == "Three Times Daily":

            meals = [

                "Breakfast",

                "Lunch",

                "Dinner"

            ]

        else:

            meals = []

        for meal in meals:

            if meal in meal_set:

                continue

            meal_set.add(meal)

            meal_reminders.append({

                "time":

                meal_times[meal],

                "type":

                "Meal",

                "meal":

                meal,

                "voice_text":

                f"It is time for your {meal.lower()}.",

                "notification_text":

                f"Please have your {meal.lower()}.",

                "priority":

                "Normal"

            })

    # Add meal reminders as one separate group
    if meal_reminders:

        reminder_groups.append(

            meal_reminders

        )

    # ------------------------------------
    # Apply AI interaction gap
    # ------------------------------------

    '''if (

        ai_schedule

        and

        ai_schedule.get("has_suggestion")

    ):

        gap = ai_schedule.get(

            "recommended_gap",

            0

        )

        reminder_groups = adjust_interaction_gap_between_medicines(

            reminder_groups,

            gap

        )'''
    if (

    ai_schedule

    and

    ai_schedule.get("adjustments")

):

        reminder_groups = adjust_interaction_gap_pairwise(

            reminder_groups,

            

            ai_schedule

    )

    return reminder_groups   

'''def reminder_times_for_database(reminder_group):
    """
    Convert reminder objects into database reminder_time string.

    Example:
    [
        Meal 09:30,
        Medicine 10:00,
        Meal 20:30,
        Medicine 21:00
    ]

    Returns:
        "10:00,21:00"
    """

    medicine_times = []

    for reminder in reminder_group:

        if reminder["type"] == "Medicine":

            medicine_times.append(
                reminder["time"]
            )

    return ",".join(medicine_times) '''


'''if __name__ == "__main__":

    sample = {

        "medicine": "Dolo 650",

        "dose": "1 tablet",

        "frequency": "Twice Daily",

        "instruction": "After Food"

    }

    reminders = build_reminders(sample)

    print()

    for reminder in reminders:

        print(reminder)'''

'''if __name__ == "__main__":

    medicines = [

        {

            "medicine":"Pan 40",

            "dose":"1 tablet",

            "frequency":"Once Daily",

            "instruction":"Before Food"

        },

        {

            "medicine":"Dolo 650",

            "dose":"1 tablet",

            "frequency":"Twice Daily",

            "instruction":"After Food"

        }

    ]

    ai_schedule = {

        "has_suggestion": True,

        "recommended_gap": 60

    }

    reminders = generate_reminder_times(

        medicines,

        ai_schedule

    )

    from pprint import pprint

    pprint(reminders)
    print()

    print("Database Times")

    for group in reminders:

       print(

        reminder_times_for_database(

            group

        )

    )'''