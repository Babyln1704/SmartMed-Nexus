import csv

with open("medicines.csv", "r") as file:
    reader = csv.DictReader(file)
    medicine_data = list(reader)

medicine = medicine_data[0]

while True:
    user = input("You: ").lower()

    if "medicine" in user:
        print("Bot:", medicine["Medicine"])

    elif "dose" in user:
        print("Bot:", medicine["Dose"])

    elif "frequency" in user:
        print("Bot:", medicine["Frequency"])

    elif "exit" in user:
        print("Bot: Goodbye!")
        break

    else:
        print("Bot: Please ask about medicine, dose, or frequency.")