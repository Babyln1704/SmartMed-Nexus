import csv

medicine = "Paracetamol 500mg"
dose = "1 tablet after food"
frequency = "Twice daily"

with open("medicines.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Medicine", "Dose", "Frequency"])
    writer.writerow([medicine, dose, frequency])

print("Medicine saved successfully!")