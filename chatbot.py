while True:
    user = input("You: ").lower()

    if "medicine" in user:
        print("Bot: Your medicine is Paracetamol 500mg")

    elif "dose" in user:
        print("Bot: Take 1 tablet after food")

    elif "frequency" in user:
        print("Bot: Twice daily")

    elif "exit" in user:
        print("Bot: Goodbye!")
        break

    else:
        print("Bot: Sorry, I don't understand.")