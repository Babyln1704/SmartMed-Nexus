from datetime import datetime, timedelta

medicine = "Paracetamol 500mg"
frequency = "Twice daily"

current_time = datetime.now()

print("Medicine:", medicine)
print("Current Time:", current_time.strftime("%H:%M"))

if frequency.lower() == "twice daily":
    next_dose = current_time + timedelta(hours=12)
elif frequency.lower() == "once daily":
    next_dose = current_time + timedelta(days=1)
else:
    next_dose = current_time + timedelta(hours=8)

print("Next Dose Time:", next_dose.strftime("%Y-%m-%d %H:%M"))