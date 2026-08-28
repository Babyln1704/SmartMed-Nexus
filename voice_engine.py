"""
=========================================
SmartMed AI
Voice Reminder Engine
=========================================
"""

import pyttsx3
import threading
import speech_recognition as sr
speech_lock = threading.Lock()

# =========================================
# INITIALIZE
# =========================================



engine = pyttsx3.init()

engine.setProperty("rate", 160)

engine.setProperty("volume", 1.0)

LANGUAGE_CODES = {

    "en": "en-IN",

    "kn": "kn-IN",

    "hi": "hi-IN",

    "ta": "ta-IN",

    "te": "te-IN"

}


# =========================================
# SPEAK
# =========================================

def speak(text):

    print("VOICE :", text)

    engine.say(text)

    engine.runAndWait()


# =========================================
# CREATE VOICE MESSAGE
# =========================================

def create_voice_message(reminder):

    reminder_type = reminder["type"]

    if reminder_type == "Meal":

        meal = reminder["meal"]

        if meal == "Breakfast":

            return (
                "Good Morning. "
                "Please have your breakfast."
            )

        elif meal == "Lunch":

            return (
                "Good Afternoon. "
                "Please have your lunch."
            )

        elif meal == "Dinner":

            return (
                "Good Evening. "
                "Please have your dinner."
            )

    elif reminder_type == "Medicine":

        medicine = reminder["medicine"]

        dose = reminder["dose"]

        instruction = reminder["instruction"]

        if dose != "Not Found":

            return (

                f"It is time to take "

                f"{dose} of "

                f"{medicine} "

                f"{instruction.lower()}."

            )

        return f"It is time to take {medicine}."

    return reminder["voice_text"]


# =========================================
# SPEAK REMINDER
# =========================================

def speak_reminder(reminder):

    message = create_voice_message(reminder)

    speak(message)


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    reminder = {

        "type":"Medicine",

        "medicine":"Dolo 650",

        "dose":"1 tablet",

        "instruction":"After Food",

        "voice_text":""

    }

    speak_reminder(reminder)

def listen_command(language="en"):

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print("🎤 Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=5
            )

        print("Recognizing...")

        text = recognizer.recognize_google(

            audio,

            language=LANGUAGE_CODES.get(
                language,
                "en-IN"
            )

        )

        print("You said:", text)

        return text.lower()

    except sr.UnknownValueError:

        return ""

    except sr.RequestError:

        return ""

    except Exception as e:

        print(e)

        return ""
    
'''def execute_command(command):

    command = command.lower().strip()

    # --------------------------------------------------
    # If user is asking a QUESTION
    # Let process_question() answer it
    # --------------------------------------------------

    QUESTION_WORDS = [

        "what",
        "when",
        "which",
        "how",
        "tell",
        
        
        "do i",
        "did i",
        "can i",
        "next",

        "ಏನು",
        "ಯಾವ",
        "ಎಷ್ಟು",

        "क्या",
        "कौन",
        "कब",
        "कितना",

        "என்ன",
        "எப்போது",

        "ఏమి",
        "ఎప్పుడు"

    ]

    

    # --------------------------------------------------
    # Navigation Commands ONLY
    # --------------------------------------------------

    if "open dashboard" in command:
        return "/dashboard"

    if "dashboard" == command:
        return "/dashboard"

    if "show reminders" in command:
        return "/reminders"

    if command == "reminders":
        return "/reminders"

    if "show medicines" in command:
      return "/my_medicines"
    
    if "next reminder" in command:
      return "/next_medicine"

    if "emergency contact" in command:
        return "/emergency_contact"

    if command == "emergency":
        return "/emergency_contact"

    return None

    if any(word in command for word in QUESTION_WORDS):

        return None'''

def execute_command(command):

    command = command.lower().strip()

    # ==================================================
    # NAVIGATION COMMANDS
    # ==================================================

    # Dashboard
    if "open dashboard" in command or command == "dashboard":
        return "/dashboard"

    # Medicines
    if (
        "show medicines" in command or
        "medicine list" in command or
        "list medicines" in command or
        command == "medicines"
    ):
        return "/my_medicines"

    # Reminders
    if (
        "show reminders" in command or
        "reminder list" in command or
        "list reminders" in command or
        command == "reminders"
    ):
        return "/reminders"

    # Next Reminder
    if (
        "next reminder" in command or
        "next medicine" in command
    ):
        return "/next_medicine"

    # Emergency Contact
    if (
        "emergency contact" in command or
        command == "emergency"
    ):
        return "/emergency_contact"

    # ==================================================
    # QUESTIONS → Let process_question() answer them
    # ==================================================

    QUESTION_WORDS = [

        "what",
        "when",
        "which",
        "how",
        "tell",
        "do i",
        "did i",
        "can i",

        "ಏನು",
        "ಯಾವ",
        "ಎಷ್ಟು",

        "क्या",
        "कौन",
        "कब",
        "कितना",

        "என்ன",
        "எப்போது",

        "ఏమి",
        "ఎప్పుడు"

    ]

    if any(word in command for word in QUESTION_WORDS):
        return None

    # Everything else
    return None

def speak_text(text, lang="en"):

    print(">>> SPEAKING:", text)

    with speech_lock:

        try:

            engine.stop()

        except:
            pass

        engine.say(text)

        engine.runAndWait()

    print(">>> FINISHED")    

