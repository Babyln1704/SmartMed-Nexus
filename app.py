from datetime import datetime
from medicine_extractor import extract_medicines
from voice_engine import listen_command, execute_command,speak_text
from interaction_service import analyze_prescription, save_medicines,get_patient_medicines,update_dashboard_reminder_times
from check import check_prescription_interactions_ai
from reminder_scheduler import generate_reminder_times
from reminder_service import save_reminders,delete_patient_reminders
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

import pytesseract



pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import sqlite3
import cv2
import csv


from flask import Response
from deep_translator import GoogleTranslator
from flask import redirect 
app = Flask(__name__)
def translate_text(text):

    lang = session.get('language', 'en')

    language_map = {
        'en': 'en',
        'kn': 'kn',
        'hi': 'hi',
        'ta': 'ta',
        'te': 'te'
    }

    target = language_map.get(lang, 'en')

    if target == 'en':
        return text

    try:
        return GoogleTranslator(
            source='auto',
            target=target
        ).translate(text)

    except:
        return text
    
    
    
UI_TEXT = {

    "en": {

        "dashboard": "Dashboard",
        "total": "Total",
        "taken": "Taken",
        "pending": "Pending",
        "adherence": "Adherence Score",
        "medicine": "Medicine",
        "dose": "Dose",
        "frequency": "Frequency",
        "reminder_time": "Reminder Time",
        "id": "ID",
        "records": "Medicine Records",
        "strength": "Strength",
        "duration": "Duration",
        "instruction": "Instruction",
        "status": "Status",
        "taken_time": "Taken Time",
        "take": "Take",
        "edit": "Edit",
        "delete": "Delete",
        "next_reminder": "Next Reminder",
        "time": "Time",
        "read_aloud": "Speak",
        "no_pending":"No pending reminders.",
        "profile_dashboard": "SmartMed Dashboard",
        "delete_patient": "Delete Patient",
        "patient_not_found": "Patient Not Found",
        "delete_confirm": "Are you sure you want to permanently delete this patient?",
        "age": "Age",
        "register_patient":"Register New Patient",
"full_name":"Full Name",
"gender":"Gender",
"male":"Male",
"female":"Female",
"other":"Other",
"phone":"Phone Number",
"emergency_contact":"Emergency Contact",
"username":"Username",
"password":"Password",
"register":"Register",
"registration_success":"User Registered Successfully!",
"go_login":"Go to Login",
        "back": "Back"

    },

    "kn": {

        "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "total": "ಒಟ್ಟು",
        "taken": "ತೆಗೆದುಕೊಂಡವು",
        "pending": "ಬಾಕಿ",
        "adherence": "ಔಷಧ ಪಾಲನಾ ಅಂಕ",
        "medicine": "ಔಷಧ",
        "dose": "ಡೋಸ್",
        "frequency": "ಆವರ್ತಿ",
        "reminder_time": "ಜ್ಞಾಪನೆ ಸಮಯ",
        "id": "ಐಡಿ",
        "records": "ಔಷಧ ದಾಖಲೆಗಳು",
        "strength": "ಶಕ್ತಿ",
        "duration": "ಅವಧಿ",
        "instruction": "ಸೂಚನೆ",
        "status": "ಸ್ಥಿತಿ",
        "taken_time": "ತೆಗೆದುಕೊಂಡ ಸಮಯ",
        "take": "ತೆಗೆದುಕೊಳ್ಳಿ",
        "edit": "ತಿದ್ದು",
        "delete": "ಅಳಿಸಿ",
        "next_reminder": "ಮುಂದಿನ ಜ್ಞಾಪನೆ",
        "time": "ಸಮಯ",
        "read_aloud": "ಜೋರಾಗಿ ಹೇಳಿ",
        "no_pending":"ಯಾವುದೇ ಬಾಕಿ ಜ್ಞಾಪನೆಗಳಿಲ್ಲ.",
        "profile_dashboard": "SmartMed ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "register_patient":"ಹೊಸ ರೋಗಿ ನೋಂದಣಿ",
"full_name":"ಪೂರ್ಣ ಹೆಸರು",
"gender":"ಲಿಂಗ",
"male":"ಪುರುಷ",
"female":"ಮಹಿಳೆ",
"other":"ಇತರೆ",
"phone":"ದೂರವಾಣಿ ಸಂಖ್ಯೆ",
"emergency_contact":"ತುರ್ತು ಸಂಪರ್ಕ",
"username":"ಬಳಕೆದಾರ ಹೆಸರು",
"password":"ಗುಪ್ತಪದ",
"register":"ನೋಂದಣಿ",
"registration_success":"ಬಳಕೆದಾರ ಯಶಸ್ವಿಯಾಗಿ ನೋಂದಾಯಿಸಲಾಗಿದೆ!",
"go_login":"ಲಾಗಿನ್‌ಗೆ ಹೋಗಿ",
"delete_patient": "ರೋಗಿಯನ್ನು ಅಳಿಸಿ",
"patient_not_found": "ರೋಗಿ ಕಂಡುಬಂದಿಲ್ಲ",
"delete_confirm": "ಈ ರೋಗಿಯನ್ನು ಶಾಶ್ವತವಾಗಿ ಅಳಿಸಲು ಖಚಿತವಾಗಿದ್ದೀರಾ?",
"age": "ವಯಸ್ಸು",
        "back": "ಹಿಂದೆ"

    },

    "hi": {

        "dashboard": "डैशबोर्ड",
        "total": "कुल",
        "taken": "ली गई",
        "pending": "बाकी",
        "adherence": "दवा पालन स्कोर",
        "medicine": "दवा",
        "dose": "खुराक",
        "frequency": "आवृत्ति",
        "reminder_time": "रिमाइंडर समय",
        "id": "आईडी",
        "records": "दवा रिकॉर्ड",
        "strength": "शक्ति",
        "duration": "अवधि",
        "instruction": "निर्देश",
        "status": "स्थिति",
        "taken_time": "ली गई समय",
        "take": "ले लें",
        "edit": "संपादित करें",
        "delete": "हटाएं",
        "next_reminder": "अगला रिमाइंडर",
        "time": "समय",
        "read_aloud": "जोर से बोलें",
        "profile_dashboard": "स्मार्टमेड डैशबोर्ड",
        "register_patient":"नया रोगी पंजीकरण",
"full_name":"पूरा नाम",
"gender":"लिंग",
"male":"पुरुष",
"female":"महिला",
"other":"अन्य",
"phone":"फोन नंबर",
"emergency_contact":"आपातकालीन संपर्क",
"username":"उपयोगकर्ता नाम",
"password":"पासवर्ड",
"register":"पंजीकरण",
"registration_success":"उपयोगकर्ता सफलतापूर्वक पंजीकृत हुआ!",
"go_login":"लॉगिन पर जाएँ",
"delete_patient": "रोगी हटाएँ",
"patient_not_found": "रोगी नहीं मिला",
"delete_confirm": "क्या आप इस रोगी को स्थायी रूप से हटाना चाहते हैं?",
"age": "आयु",
        "back": "वापस"

    },

    "ta": {

        "dashboard": "டாஷ்போர்டு",
        "total": "மொத்தம்",
        "taken": "எடுத்தவை",
        "pending": "நிலுவை",
        "adherence": "மருந்து பின்பற்றல் மதிப்பெண்",
        "medicine": "மருந்து",
        "dose": "அளவு",
        "frequency": "அடிக்கடி",
        "reminder_time": "நினைவூட்டல் நேரம்",
        "id": "அடையாள எண்",
       "records": "மருந்து பதிவுகள்",
       "strength": "வலிமை",
       "duration": "காலம்",
       "instruction": "வழிமுறை",
        "status": "நிலை",
       "taken_time": "எடுத்த நேரம்",
       "take": "எடுக்கவும்",
       "edit": "திருத்து",
       "delete": "நீக்கு",
       "next_reminder": "அடுத்த நினைவூட்டல்",
       "time": "நேரம்",
       "read_aloud": "சத்தமாக பேசுங்கள்",
       "no_pending":"நிலுவையில் நினைவூட்டல்கள் இல்லை.",
       "profile_dashboard": "ஸ்மார்ட்மெட் டாஷ்போர்டு",
       "register_patient":"புதிய நோயாளர் பதிவு",
"full_name":"முழு பெயர்",
"gender":"பாலினம்",
"male":"ஆண்",
"female":"பெண்",
"other":"மற்றவை",
"phone":"தொலைபேசி எண்",
"emergency_contact":"அவசர தொடர்பு",
"username":"பயனர் பெயர்",
"password":"கடவுச்சொல்",
"register":"பதிவு",
"registration_success":"பயனர் வெற்றிகரமாக பதிவு செய்யப்பட்டார்!",
"go_login":"உள்நுழைவுக்கு செல்லவும்",
"delete_patient": "நோயாளியை நீக்கு",
"patient_not_found": "நோயாளர் கிடைக்கவில்லை",
"delete_confirm": "இந்த நோயாளியை நிரந்தரமாக நீக்க விரும்புகிறீர்களா?",
"age": "வயது",
        "back": "பின்"

    },

    "te": {

        "dashboard": "డాష్‌బోర్డ్",
        "total": "మొత్తం",
        "taken": "తీసుకున్నవి",
        "pending": "మిగిలినవి",
        "adherence": "ఔషధ అనుసరణ స్కోరు",
        "medicine": "మందు",
        "dose": "మోతాదు",
        "frequency": "తరచుదనం",
        "reminder_time": "రిమైండర్ సమయం",
        "id": "ఐడి",
        "records": "మందుల రికార్డులు",
       "strength": "శక్తి",
      "duration": "వ్యవధి",
      "instruction": "సూచనలు",
      "status": "స్థితి",
      "taken_time": "తీసుకున్న సమయం",
      "take": "తీసుకోండి",
      "edit": "సవరించు",
      "delete": "తొలగించు",
      "next_reminder": "తదుపరి రిమైండర్",
      "time": "సమయం",
       "read_aloud": "గట్టిగా చెప్పండి",
       "no_pending":"పెండింగ్ రిమైండర్లు లేవు.",
       "profile_dashboard": "స్మార్ట్‌మెడ్ డాష్‌బోర్డ్",
       "register_patient":"కొత్త రోగి నమోదు",
"full_name":"పూర్తి పేరు",
"gender":"లింగం",
"male":"పురుషుడు",
"female":"మహిళ",
"other":"ఇతరులు",
"phone":"ఫోన్ నంబర్",
"emergency_contact":"అత్యవసర సంప్రదింపు",
"username":"వినియోగదారు పేరు",
"password":"పాస్‌వర్డ్",
"register":"నమోదు",
"registration_success":"వినియోగదారు విజయవంతంగా నమోదు అయ్యారు!",
"go_login":"లాగిన్‌కు వెళ్లండి",
"delete_patient": "రోగిని తొలగించండి",
"patient_not_found": "రోగి కనబడలేదు",
"delete_confirm": "ఈ రోగిని శాశ్వతంగా తొలగించాలనుకుంటున్నారా?",
"age": "వయస్సు",
        "back": "వెనక్కి"

    }

}

DOSE_TEXT = {

    "en": {
        "1 tablet": "1 tablet"
    },

    "kn": {
        "1 tablet": "1 ಮಾತ್ರೆ"
    },

    "hi": {
        "1 tablet": "1 गोली"
    },

    "ta": {
        "1 tablet": "1 மாத்திரை"
    },

    "te": {
        "1 tablet": "1 మాత్ర"
    }

}

FREQUENCY_TEXT = {

    "en": {

        "once daily": "Once Daily",
        "twice daily": "Twice Daily",
        "three times daily": "Three Times Daily"

    },

    "kn": {

        "once daily": "ದಿನಕ್ಕೆ ಒಮ್ಮೆ",
        "twice daily": "ದಿನಕ್ಕೆ ಎರಡು ಬಾರಿ",
        "three times daily": "ದಿನಕ್ಕೆ ಮೂರು ಬಾರಿ"

    },

    "hi": {

        "once daily": "दिन में एक बार",
        "twice daily": "दिन में दो बार",
        "three times daily": "दिन में तीन बार"

    },

    "ta": {

        "once daily": "ஒரு நாள் ஒரு முறை",
        "twice daily": "ஒரு நாள் இரண்டு முறை",
        "three times daily": "ஒரு நாள் மூன்று முறை"

    },

    "te": {

        "once daily": "రోజుకు ఒకసారి",
        "twice daily": "రోజుకు రెండుసార్లు",
        "three times daily": "రోజుకు మూడుసార్లు"

    }

}

VOICE_MESSAGES = {

    "en": {

        "medicine": "It is time to take {medicine}.",

        "meal": "It is time for {meal}."

    },

    "kn": {

        "medicine": "ಈಗ {medicine} ಔಷಧ ತೆಗೆದುಕೊಳ್ಳುವ ಸಮಯವಾಗಿದೆ.",

        "meal": "ಈಗ {meal} ಮಾಡುವ ಸಮಯವಾಗಿದೆ."

    },

    "hi": {

        "medicine": "अब {medicine} लेने का समय है।",

        "meal": "अब {meal} का समय है।"

    },

    "ta": {

        "medicine": "இப்போது {medicine} எடுத்துக்கொள்ளும் நேரம்.",

        "meal": "இப்போது {meal} நேரம்."

    },

    "te": {

        "medicine": "ఇప్పుడు {medicine} తీసుకునే సమయం వచ్చింది.",

        "meal": "ఇప్పుడు {meal} సమయం వచ్చింది."

    }

}

def TEXT(key):

    lang = session.get("language", "en")

    return UI_TEXT.get(
        lang,
        UI_TEXT["en"]
    ).get(
        key,
        key
    )
from functools import lru_cache

@lru_cache(maxsize=200)
def transliterate_name(name, lang):

    if lang == "en":
        return name

    language_map = {

        "kn": "kn",
        "hi": "hi",
        "ta": "ta",
        "te": "te"

    }

    try:

        return GoogleTranslator(

            source="auto",
            target=language_map.get(lang, "en")

        ).translate(name)

    except:

        return name
    
    
app.secret_key = "smartmed_secret_key"
from flask import redirect 

@app.route('/')
def home():

    if 'user' not in session:
        return redirect('/login')

    patient_id = session.get('patient_id')

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    patient_photo = "ravi.jpg"
    patient_name = ""

    if patient_id:

        cursor.execute(
            "SELECT * FROM patients WHERE id=?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient:
            patient_photo = patient[4]
            patient_name = transliterate_name(
    patient[2],
    session.get("language", "en")
)

    conn.close()

    return render_template(
        "index.html",
        patient_name=patient_name,
        patient_photo=patient_photo,
        lang=session.get("language", "en"),
        translate=translate_text
    )

@app.route('/register')
def register():

    return f"""

<h2>👤 {TEXT("register_patient")}</h2>

<form action="/save_user" method="POST">

{TEXT("full_name")}:
<input type="text"
name="fullname"
required>

<br><br>

{TEXT("age")}:
<input type="number"
name="age"
required>

<br><br>

{TEXT("gender")}:

<select name="gender">

<option>{TEXT("male")}</option>

<option>{TEXT("female")}</option>

<option>{TEXT("other")}</option>

</select>

<br><br>

{TEXT("phone")}:

<input type="text"
name="phone"
required>

<br><br>

{TEXT("emergency_contact")}:

<input type="text"
name="emergency_contact"
required>

<br><br>

{TEXT("username")}:

<input type="text"
name="username"
required>

<br><br>

{TEXT("password")}:

<input type="password"
name="password"
required>

<br><br>

<button type="submit">

{TEXT("register")}

</button>

</form>

"""





@app.route('/save_user', methods=['POST'])
def save_user():

    fullname = request.form['fullname']
    age = request.form['age']
    gender = request.form['gender']
    phone = request.form['phone']
    emergency_contact = request.form['emergency_contact']

    username = request.form['username']
    password = request.form['password']

    username = username.strip()

    if not username.upper().startswith("CG_"):

       messages = {

        "en": "❌ Username must start with CG_ (Example: CG_Shailaja)",

        "kn": "❌ ಬಳಕೆದಾರರ ಹೆಸರು CG_ ರಿಂದ ಪ್ರಾರಂಭವಾಗಬೇಕು. ಉದಾಹರಣೆ: CG_Shailaja",

        "hi": "❌ उपयोगकर्ता नाम CG_ से शुरू होना चाहिए। उदाहरण: CG_Shailaja",

        "ta": "❌ பயனர்பெயர் CG_ என்று தொடங்க வேண்டும். உதாரணம்: CG_Shailaja",

        "te": "❌ వినియోగదారు పేరు CG_ తో ప్రారంభం కావాలి. ఉదాహరణ: CG_Shailaja"

    }

       lang = session.get("language", "en")

       return f"""
       <h2 style="color:red;">
       {messages.get(lang, messages["en"])}
       </h2>

       <br>

       <a href="/register">
       ⬅ {TEXT("register")}
       </a>
    """

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users
    (fullname, age, gender, phone,
     emergency_contact, username, password)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        fullname,
        age,
        gender,
        phone,
        emergency_contact,
        username,
        password
    ))

    conn.commit()
    conn.close()

    return f"""

    <h2>

✅ {TEXT("registration_success")}

    </h2>

    <a href="/login">

    {TEXT("go_login")}

</a>

"""


@app.route('/login')
def login():

    if 'user' in session:
        return redirect('/')

    lang = session.get('language', 'en')

    return f"""
    <div style="text-align:right;padding:10px;">

      <select onchange="window.location.href='/set_language/' + this.value">

       <option value="en" {"selected" if lang=="en" else ""}>English</option>

<option value="kn" {"selected" if lang=="kn" else ""}>ಕನ್ನಡ</option>

<option value="hi" {"selected" if lang=="hi" else ""}>हिन्दी</option>

<option value="ta" {"selected" if lang=="ta" else ""}>தமிழ்</option>

<option value="te" {"selected" if lang=="te" else ""}>తెలుగు</option>

        </select> 

    </div>

    <h2>{
"ಸ್ಮಾರ್ಟ್‌ಮೆಡ್  ಲಾಗಿನ್" if lang=="kn"
else "स्मार्टमेड  लॉगिन" if lang=="hi"
else "ஸ்மார்ட்மெட்  உள்நுழைவு" if lang=="ta"
else "స్మార్ట్‌మెడ్  లాగిన్" if lang=="te"
else "SmartMed  Login"
}</h2>

    <form action='/check_login' method='POST'>

        {
"ಬಳಕೆದಾರ ಹೆಸರು" if lang=="kn"
else "उपयोगकर्ता नाम" if lang=="hi"
else "பயனர் பெயர்" if lang=="ta"
else "వినియోగదారు పేరు" if lang=="te"
else "Username"
}:
        <input type='text' name='username'>

        <br><br>

      {
"ಪಾಸ್‌ವರ್ಡ್" if lang=="kn"
else "पासवर्ड" if lang=="hi"
else "கடவுச்சொல்" if lang=="ta"
else "పాస్‌వర్డ్" if lang=="te"
else "Password"
}:
        <input type='password' name='password'>

        <br><br>

        <button type='submit'>
       {
"ಲಾಗಿನ್" if lang=="kn"
else "लॉगिन" if lang=="hi"
else "உள்நுழை" if lang=="ta"
else "లాగిన్" if lang=="te"
else "Login"
}
        </button>

    </form>

    <br>

    <p>

{
"ಹೊಸ ಬಳಕೆದಾರ?" if lang=="kn"
else "नया उपयोगकर्ता?" if lang=="hi"
else "புதிய பயனர்?" if lang=="ta"
else "కొత్త వినియోగదారు?" if lang=="te"
else "New User?"
}

<a href="/register">

📝{
"ಇಲ್ಲಿ ನೋಂದಣಿ ಮಾಡಿ" if lang=="kn"
else "यहाँ पंजीकरण करें" if lang=="hi"
else "இங்கே பதிவு செய்யவும்" if lang=="ta"
else "ఇక్కడ నమోదు చేయండి" if lang=="te"
else "Register Here"
}

</a>

</p>
    """
@app.route('/check_login', methods=['POST'])
def check_login():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        session['user'] = username
        

        return redirect('/caregiver_dashboard')

    else:

        return """
        <h2>❌ Invalid Username or Password</h2>

        <a href='/login'>
        Try Again
        </a>
        """
    

@app.route('/set_language/<lang>')
def set_language(lang):

    session['language'] = lang

    return redirect('/login')
   

@app.route('/upload', methods=['POST'])
def upload():

    image = request.files['image']
    patient_id = session.get("patient_id")

    image_path = f"uploaded_{patient_id}.jpg"

    image.save(image_path)

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    #text = pytesseract.image_to_string(gray)
    text = pytesseract.image_to_string(gray, config="--oem 3 --psm 6")
    print("\n========== OCR TEXT ==========")
    print(text)
    print("==============================")

    patient_id = session.get("patient_id")
    print("Current Patient ID:", patient_id)

    if patient_id is None:
        return "No patient selected."

    result = analyze_prescription(
        patient_id=patient_id,
        ocr_text=text
    )
    if result.get("duplicate_prescription"):

        return render_template(
        "upload_success.html",
        duplicate=True,
        message=result["message"],
        lang=session.get("language","en")
    )
    print("\n========== AI SCHEDULE ==========")
    print(result["ai_schedule"])

    # No interaction → behave exactly like friend's project
    if not result["ai_schedule"]["has_suggestion"]:

        save_medicines(
            patient_id,
            #result[]
            result["parsed_medicines"],
            result["ai_schedule"]
        )
        # ----------------------------------
# Generate Smart AI Reminders
# ----------------------------------

        reminder_groups = generate_reminder_times(

            result["parsed_medicines"],

            result["ai_schedule"]

)

        save_reminders(

            patient_id,

            reminder_groups

)
        session.pop("pending_patient", None)
        session.pop("pending_medicines", None)

        return render_template(
    "upload_success.html",
    medicines=result["new_medicines"],
    lang=session.get("language","en")
)

    # Interaction → store temporarily
    session["pending_patient"] = patient_id
    session["pending_medicines"] = result["parsed_medicines"]
    session["pending_ai_schedule"] = result["ai_schedule"]

    return render_template(
        "analysis_result_final.html",
        result=result,
        lang=session.get("language", "en")
    )

@app.route("/confirm_upload", methods=["POST"])
def confirm_upload():

    patient_id = session.get("pending_patient")
    medicines = session.get("pending_medicines")

    mode = request.form.get("mode")

    if patient_id and medicines:

        # --------------------------
        # Replace Existing Medicines
        # --------------------------

        if mode == "replace":

            conn = sqlite3.connect("medicine.db")
            cursor = conn.cursor()

            cursor.execute("""

                DELETE FROM medicines

                WHERE patient_id = ?

            """, (patient_id,))

            conn.commit()
            conn.close()

            delete_patient_reminders(patient_id)

        # ------------------------------------
        # Save medicines
        # ------------------------------------

        save_medicines(

            patient_id,

            medicines,

            session.get("pending_ai_schedule")

        )

        all_medicines = get_patient_medicines(

            patient_id

        )

        print("\n========== ALL MEDICINES ==========")

        for med in all_medicines:

            print(med)

        delete_patient_reminders(

            patient_id

        )

        # ------------------------------------
        # Reminder Generation
        # ------------------------------------

        if mode == "replace":

            reminder_groups = generate_reminder_times(

                all_medicines,

                None

            )

        else:

            reminder_groups = generate_reminder_times(

                all_medicines,

                session.get("pending_ai_schedule")

            )

        save_reminders(

            patient_id,

            reminder_groups

        )
        update_dashboard_reminder_times(

    patient_id,

    reminder_groups

)

    session.pop("pending_patient", None)
    session.pop("pending_medicines", None)
    session.pop("pending_ai_schedule", None)

    return redirect(url_for("dashboard"))
   




  
    
@app.route('/exit_patient')
def exit_patient():

    session.pop('patient_id', None)
    session.pop('patient_name', None)

    return redirect('/caregiver_dashboard')


@app.route('/view')
def view():

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    patient_id = session["patient_id"]

    cursor.execute("""
    SELECT *
    FROM medicines
    WHERE patient_id=?
    """, (patient_id,))

    data = cursor.fetchall()

    conn.close()

    lang = session.get("language", "en")

    html = f"""
    <h2>{TEXT("records")}</h2>

    <table border='1' cellpadding='10'>

    <tr>

        <th>{TEXT("id")}</th>
        <th>{TEXT("medicine")}</th>
        <th>{TEXT("strength")}</th>
        <th>{TEXT("dose")}</th>
        <th>{TEXT("frequency")}</th>
        <th>{TEXT("duration")}</th>
        <th>{TEXT("instruction")}</th>
        <th>{TEXT("reminder_time")}</th>
        <th>{TEXT("status")}</th>
        <th>{TEXT("taken_time")}</th>
        
        <th>{TEXT("edit")}</th>
        <th>{TEXT("delete")}</th>

    </tr>
    """

    for row in data:

        dose = DOSE_TEXT.get(
            lang,
            DOSE_TEXT["en"]
        ).get(
            row[2].strip().lower(),
            row[2]
        )

        frequency = FREQUENCY_TEXT.get(
            lang,
            FREQUENCY_TEXT["en"]
        ).get(
            row[3].strip().lower(),
            row[3]
        )

        status = (
            f"<span style='color:green;font-weight:bold;'>✅ {TEXT('taken')}</span>"
            if row[5] == "Taken"
            else
            f"<span style='color:red;font-weight:bold;'>⏳ {TEXT('pending')}</span>"
        )

        html += f"""

        <tr>

            <td>{row[0]}</td>

            <td>{row[1]}</td>

            <td>{row[9] if row[9] else "-"}</td>

            <td>{dose}</td>

            <td>{frequency}</td>

            <td>{row[10] if row[10] else "-"}</td>

            <td>{translate_text(row[11]) if row[11] else "-"}</td>

            <td>{row[4]}</td>

            <td>{status}</td>

            <td>{row[6] if row[6] else "-"}</td>

            

            <td>
                <a href="/edit/{row[0]}">
                    {TEXT("edit")}
                </a>
            </td>

            <td>
                <a href="/delete/{row[0]}">
                    {TEXT("delete")}
                </a>
            </td>

        </tr>

        """

    html += "</table>"

    return html


@app.route('/edit/<int:id>')
def edit(id):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM medicines WHERE id=?",
        (id,)
    )

    medicine = cursor.fetchone()

    conn.close()

    lang = session.get("language", "en")

    title = (
        "ಔಷಧವನ್ನು ಸಂಪಾದಿಸಿ" if lang=="kn"
        else "दवा संपादित करें" if lang=="hi"
        else "மருந்தை திருத்து" if lang=="ta"
        else "ఔషధాన్ని సవరించండి" if lang=="te"
        else "Edit Medicine"
    )

    medicine_text = (
        "ಔಷಧ" if lang=="kn"
        else "दवा" if lang=="hi"
        else "மருந்து" if lang=="ta"
        else "ఔషధం" if lang=="te"
        else "Medicine"
    )

    dose_text = (
        "ಡೋಸ್" if lang=="kn"
        else "खुराक" if lang=="hi"
        else "அளவு" if lang=="ta"
        else "మోతాదు" if lang=="te"
        else "Dose"
    )

    frequency_text = (
        "ಆವರ್ತಿ" if lang=="kn"
        else "आवृत्ति" if lang=="hi"
        else "அடிக்கடி" if lang=="ta"
        else "తరచుదనం" if lang=="te"
        else "Frequency"
    )

    reminder_text = (
        "ಜ್ಞಾಪನೆ ಸಮಯ" if lang=="kn"
        else "रिमाइंडर समय" if lang=="hi"
        else "நினைவூட்டும் நேரம்" if lang=="ta"
        else "రిమైండర్ సమయం" if lang=="te"
        else "Reminder Time"
    )

    update_text = (
        "ನವೀಕರಿಸಿ" if lang=="kn"
        else "अपडेट करें" if lang=="hi"
        else "புதுப்பிக்கவும்" if lang=="ta"
        else "నవీకరించండి" if lang=="te"
        else "Update"
    )

    dose_value = DOSE_TEXT.get(
        lang,
        DOSE_TEXT["en"]
    ).get(
        medicine[2],
        medicine[2]
    )

    frequency_value = FREQUENCY_TEXT.get(
        lang,
        FREQUENCY_TEXT["en"]
    ).get(
        medicine[3],
        medicine[3]
    )

    return f"""

    <h2>{title}</h2>

    <form action='/update/{id}' method='POST'>

        {medicine_text}:
        <input type='text'
               name='medicine'
               value='{medicine[1]}'>

        <br><br>

        {dose_text}:
        <input type='text'
               name='dose'
               value='{dose_value}'>

        <br><br>

        {frequency_text}:
        <input type='text'
               name='frequency'
               value='{frequency_value}'>

        <br><br>

        {reminder_text}:
        <input type='text'
               name='reminder'
               value='{medicine[4]}'>

        <br><br>

        <button type='submit'>
            {update_text}
        </button>

    </form>

    """

@app.route('/medicines')
def medicines():

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medicines")
    data = cursor.fetchall()

    conn.close()

    return jsonify(data)


@app.route('/search')
def search():

    medicine_name = request.args.get('name')

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    patient_id = session.get("patient_id")

    cursor.execute("""
SELECT *

FROM medicines

WHERE
patient_id=?

AND
medicine LIKE ?
""",
(
    patient_id,
    "%" + medicine_name + "%"
))

    data = cursor.fetchall()

    conn.close()

    return jsonify(data)



@app.route('/reminders')
def reminders():

    patient_id = session.get("patient_id")
    lang = session.get("language", "en")

    if patient_id is None:
        return redirect(url_for("login"))

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        reminder_time,
        reminder_type,
        medicine,
        meal,
        status
    FROM reminders
    WHERE patient_id=?
    ORDER BY reminder_time
    """, (patient_id,))

    reminders = cursor.fetchall()

    conn.close()

    TEXT = {

        "title":{
            "en":"🔔 SmartMed  Reminders",
            "kn":"🔔 SmartMed  ಜ್ಞಾಪನೆಗಳು",
            "hi":"🔔 स्मार्टमेड रिमाइंडर",
            "ta":"🔔 ஸ்மார்ட்மெட்  நினைவூட்டல்கள்",
            "te":"🔔 స్మార్ట్‌మెడ్  రిమైండర్లు"
        },

        "time":{
            "en":"Time",
            "kn":"ಸಮಯ",
            "hi":"समय",
            "ta":"நேரம்",
            "te":"సమయం"
        },

        "type":{
            "en":"Type",
            "kn":"ವಿಧ",
            "hi":"प्रकार",
            "ta":"வகை",
            "te":"రకం"
        },

        "reminder":{
            "en":"Reminder",
            "kn":"ಜ್ಞಾಪನೆ",
            "hi":"रिमाइंडर",
            "ta":"நினைவூட்டல்",
            "te":"రిమైండర్"
        },

        "status":{
            "en":"Status",
            "kn":"ಸ್ಥಿತಿ",
            "hi":"स्थिति",
            "ta":"நிலை",
            "te":"స్థితి"
        },

        "action":{
            "en":"Action",
            "kn":"ಕ್ರಿಯೆ",
            "hi":"कार्य",
            "ta":"செயல்",
            "te":"చర్య"
        },

        "medicine":{
            "en":"Medicine",
            "kn":"ಔಷಧಿ",
            "hi":"दवा",
            "ta":"மருந்து",
            "te":"మందు"
        },

        "meal":{
            "en":"Meal",
            "kn":"ಊಟ",
            "hi":"भೋಜन",
            "ta":"உணவு",
            "te":"భోజనం"
        },

        "pending":{
            "en":"Pending",
            "kn":"ಬಾಕಿ",
            "hi":"लंबित",
            "ta":"நிலுவையில்",
            "te":"పెండింగ్"
        },

        "done": {
    "en":"Taken",
    "kn":"ತೆಗೆದುಕೊಳ್ಳಲಾಗಿದೆ",
    "hi":"ले लिया गया",
    "ta":"எடுத்துக்கொள்ளப்பட்டது",
    "te":"తీసుకున్నారు"
        },

        "take":{
            "en":"Take",
            "kn":"ತೆಗೆದುಕೊಳ್ಳಿ",
            "hi":"ले लें",
            "ta":"எடுத்துக்கொள்ளுங்கள்",
            "te":"తీసుకోండి"
        },

        "dashboard":{
            "en":"Dashboard",
            "kn":"ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            "hi":"डैशबोर्ड",
            "ta":"டாஷ்போர்டு",
            "te":"డాష్‌బోర్డ్"
        }

    }

    html = f"""
    <h1>{TEXT["title"][lang]}</h1>

    <table border='1' cellpadding='10'>

    <tr>

    <th>{TEXT["time"][lang]}</th>

    <th>{TEXT["type"][lang]}</th>

    <th>{TEXT["reminder"][lang]}</th>

    <th>{TEXT["status"][lang]}</th>

    <th>{TEXT["action"][lang]}</th>

    </tr>
    """

    for reminder_id, time, rtype, medicine, meal, status in reminders:

        if status == "Done":

            status_html = f"""
            <span style='color:green;'>
            ✅ {TEXT["done"][lang]}
            </span>
            """

        else:

            status_html = f"""
            <span style='color:red;'>
            ⏳ {TEXT["pending"][lang]}
            </span>
            """

        if rtype == "Meal":

            type_name = TEXT["meal"][lang]

            reminder = f"🍽 {meal}"

            action = "-"

        else:

            type_name = TEXT["medicine"][lang]

            reminder = f"💊 {medicine}"

            if status == "Pending":

                action = f"""
                <a href="/mark_reminder_taken/{reminder_id}">
                <button>
                ✅ {TEXT["take"][lang]}
                </button>
                </a>
                """

            else:

                action = "-"

        html += f"""

        <tr>

        <td>{time}</td>

        <td>{type_name}</td>

        <td>{reminder}</td>

        <td>{status_html}</td>

        <td>{action}</td>

        </tr>

        """

    html += f"""

    </table>

    <br>

    <a href="/dashboard">

    <button>

    ⬅ {TEXT["dashboard"][lang]}

    </button>

    </a>

    """

    return html

@app.route('/dashboard')
def dashboard():

    patient_id = session.get("patient_id")
   
    

    if patient_id is None:
        return redirect(url_for("login"))


    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
SELECT COUNT(*)
FROM medicines
WHERE patient_id=?
""", (patient_id,))
    total_medicines = cursor.fetchone()[0]

    cursor.execute("""
SELECT COUNT(*)
FROM medicines
WHERE
taken='Taken'
AND
patient_id=?
""", (patient_id,))
    taken_count = cursor.fetchone()[0]

    cursor.execute("""
SELECT COUNT(*)
FROM medicines
WHERE
taken='Pending'
AND
patient_id=?
""", (patient_id,))
    
    pending_count = cursor.fetchone()[0]

    if total_medicines > 0:
        adherence = round(
            (taken_count / total_medicines) * 100,
            2
        )
    else:
        adherence = 0

    cursor.execute("""
SELECT
medicine,
dose,
Frequency,                   
reminder_time

FROM medicines

WHERE patient_id=?

""",(patient_id,))

    data = cursor.fetchall()

    conn.close()
    lang = session.get("language", "en")
    

    html = f"""
    <h1>SmartMed  {TEXT("dashboard")}</h1>

    <div style='display:flex;gap:20px;'>

    <div style='background:#dbeafe;
                padding:20px;
                border-radius:10px;
                width:200px;'>

    <h2>💊 {TEXT("total")}</h2>
    <h1>{total_medicines}</h1>

    </div>

    <div style='background:#dcfce7;
                padding:20px;
                border-radius:10px;
                width:200px;'>

    <h2>✅ {TEXT("taken")}</h2>            
    <h1>{taken_count}</h1>

    </div>

    <div style='background:#fee2e2;
                padding:20px;
                border-radius:10px;
                width:200px;'>

    <h2>⏳ {TEXT("pending")}</h2>
    <h1>{pending_count}</h1>

    </div>

    </div>

    <br>

    <div style='background:#fef3c7;
                padding:20px;
                border-radius:10px;
                width:300px;'>

    <h2>📈 {TEXT("adherence")}</h2>
    <h1>{adherence}%</h1>

    </div>

    <br><br>

    <table border='1' cellpadding='10'>
    <tr>
       <th>{TEXT("medicine")}</th>
       <th>{TEXT("dose")}</th>
       <th>{TEXT("frequency")}</th>
       <th>{TEXT("reminder_time")}</th>

    </tr>
    """

    for row in data:

        dose = DOSE_TEXT.get(
    lang,
    DOSE_TEXT["en"]
).get(
    row[1].strip().lower(),
    row[1]
)

        frequency = FREQUENCY_TEXT.get(
    lang,
    FREQUENCY_TEXT["en"]
).get(
    row[2].strip().lower(),
    row[2]
)
      

        html += f"""
        <tr>

            <td>{row[0]}</td>

            <td>{dose}</td>

            <td>{frequency}</td>

            <td>{row[3]}</td>

        </tr>
        """

    html += "</table>"

    return html


@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM medicines WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    lang = session.get("language", "en")

    title = (
        "ಔಷಧವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಅಳಿಸಲಾಗಿದೆ!" if lang=="kn"
        else "दवा सफलतापूर्वक हटा दी गई!" if lang=="hi"
        else "மருந்து வெற்றிகரமாக நீக்கப்பட்டது!" if lang=="ta"
        else "ఔషధం విజయవంతంగా తొలగించబడింది!" if lang=="te"
        else "Medicine Deleted Successfully!"
    )

    back = (
        "ದಾಖಲೆಗಳಿಗೆ ಹಿಂತಿರುಗಿ" if lang=="kn"
        else "रिकॉर्ड पर वापस जाएँ" if lang=="hi"
        else "பதிவுகளுக்கு திரும்பு" if lang=="ta"
        else "రికార్డులకు తిరిగి వెళ్ళండి" if lang=="te"
        else "Go Back"
    )

    return f"""

    <h2>🗑 {title}</h2>

    <a href="/view">
        {back}
    </a>

    """

@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    medicine = request.form['medicine']
    dose = request.form['dose']
    frequency = request.form['frequency']
    reminder = request.form['reminder']

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE medicines
    SET medicine=?,
        dose=?,
        frequency=?,
        reminder_time=?
    WHERE id=?
    """,
    (
        medicine,
        dose,
        frequency,
        reminder,
        id
    ))

    conn.commit()
    conn.close()

    lang = session.get("language", "en")

    title = (
        "ಔಷಧವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ!" if lang=="kn"
        else "दवा सफलतापूर्वक अपडेट की गई!" if lang=="hi"
        else "மருந்து வெற்றிகரமாக புதுப்பிக்கப்பட்டது!" if lang=="ta"
        else "ఔషధం విజయవంతంగా నవీకరించబడింది!" if lang=="te"
        else "Medicine Updated Successfully!"
    )

    back = (
        "ದಾಖಲೆಗಳಿಗೆ ಹಿಂತಿರುಗಿ" if lang=="kn"
        else "रिकॉर्ड पर वापस जाएँ" if lang=="hi"
        else "பதிவுகளுக்கு திரும்பு" if lang=="ta"
        else "రికార్డులకు తిరిగి వెళ్ళండి" if lang=="te"
        else "Go Back"
    )

    return f"""

    <h2>✅ {title}</h2>

    <a href='/view'>{back}</a>

    """


@app.route('/export')
def export():

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    patient_id = session.get("patient_id")

    cursor.execute("""
SELECT *

FROM medicines

WHERE patient_id=?
""", (patient_id,))
    data = cursor.fetchall()

    conn.close()

    def generate():
        yield "ID,Medicine,Dose,Frequency,Reminder Time\n"

        for row in data:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=medicines.csv"
        }
    )




@app.route('/caregiver_dashboard')
def caregiver_dashboard():

    if 'user' not in session:
        return redirect('/login')

    lang = session.get('language', 'en')

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM patients
    WHERE caregiver_username=?
    """, (session['user'],))

    patients = cursor.fetchall()

    conn.close()

    dashboard_title = {
        "kn": "ಆರೈಕೆದಾರ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "hi": "देखभालकर्ता डैशबोर्ड",
        "ta": "பராமரிப்பாளர் டாஷ்போர்டு",
        "te": "సంరక్షకుల డాష్‌బోర్డ్"
    }.get(lang, "Caregiver Dashboard")

    add_patient_text = {
        "kn": "ರೋಗಿಯನ್ನು ಸೇರಿಸಿ",
        "hi": "रोगी जोड़ें",
        "ta": "நோயாளியை சேர்",
        "te": "రోగిని చేర్చండి"
    }.get(lang, "Add Patient")

    logout_text = {
        "kn": "ಲಾಗ್ ಔಟ್",
        "hi": "लॉगआउट",
        "ta": "வெளியேறு",
        "te": "లాగౌట్"
    }.get(lang, "Logout")

    html = f"""
    <html>
    <body style='font-family:Segoe UI;background:#f5f5f5;'>

    <h1> {dashboard_title}</h1>

    <div style='display:flex;gap:20px;flex-wrap:wrap;'>
    """

    for patient in patients:
        print(patient)
        print(patient[4])
        name = patient[2]

        if lang == "kn":
            if name == "Ravi Kumar":
                name = "ರವಿ ಕುಮಾರ್"
            elif name == "Lakshmi Devi":
                name = "ಲಕ್ಷ್ಮಿ ದೇವಿ"
            elif name == "Suresh Kumar":
                name = "ಸುರೇಶ್ ಕುಮಾರ್"

        elif lang == "hi":
            if name == "Ravi Kumar":
                name = "रवि कुमार"
            elif name == "Lakshmi Devi":
                name = "लक्ष्मी देवी"
            elif name == "Suresh Kumar":
                name = "सुरेश कुमार"

        elif lang == "ta":
            if name == "Ravi Kumar":
                name = "ரவிகுமார்"
            elif name == "Lakshmi Devi":
                name = "லட்சுமி தேவி"
            elif name == "Suresh Kumar":
                name = "சுரேஷ் குமார்"

        elif lang == "te":
            if name == "Ravi Kumar":
                name = "రవి కుమార్"
            elif name == "Lakshmi Devi":
                name = "లక్ష్మీ దేవి"
            elif name == "Suresh Kumar":
                name = "సురేష్ కుమార్"

        html += f"""
        <div style='background:white;
            padding:0;
            border-radius:15px;
            width:260px;
            overflow:hidden;
            box-shadow:0px 4px 15px rgba(0,0,0,0.2);'>

           <a href='/patient/{patient[0]}'
   style='text-decoration:none;'>

<img src='/static/{patient[4]}'
     style='width:100%;
            height:320px;
            object-fit:cover;
            cursor:pointer;'>

</a>

           
        </div>
        """

    html += f"""
        <div style='background:white;
                    padding:20px;
                    border-radius:15px;
                    width:220px;
                    text-align:center;
                    box-shadow:0px 4px 10px rgba(0,0,0,0.2);'>

            <a href='/add_patient'>
                <h1 style='font-size:80px;'>+</h1>
            </a>

            <p>{add_patient_text}</p>

        </div>

    </div>

    <br><br>

    <a href='/logout'>
        <button>{logout_text}</button>
    </a>

    </body>
    </html>
    """

    return html

@app.route('/logout')
def logout():


 session.pop('user', None)
 session.pop('patient_id', None)
 session.pop('patient_name', None)

 return redirect('/login')


@app.route('/patient/<int:patient_id>')
def patient_dashboard(patient_id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM patients
    WHERE id=?
    """, (patient_id,))

    patient = cursor.fetchone()

    if not patient:
        conn.close()
        return TEXT("patient_not_found")

    session['patient_id'] = patient[0]
    session['patient_name'] = patient[2]

    photo = patient[4]
    name = patient[2]
    age = patient[3]

    conn.close()

    # -----------------------------------
    # Automatically transliterate
    # patient name to selected language
    # -----------------------------------

    lang = session.get("language", "en")

    name = transliterate_name(
        name,
        lang
    )

    print("PHOTO =", photo)

    return f"""

<html>

<head>

<title>{TEXT("profile_dashboard")}</title>

</head>

<body style="
font-family:Segoe UI;
background:#f5f5f5;
text-align:center;">

<br>

<img src="/static/{photo}"
     width="170"
     height="170"
     style="
     border-radius:50%;
     border:5px solid #4CAF50;">

<h1>👤 {name}</h1>

<h3>{TEXT("age")}: {age}</h3>

<br>

<a href="/">

<button
style="
padding:15px;
width:220px;
font-size:18px;">

📊 {TEXT("profile_dashboard")}

</button>

</a>

<br><br>

<a href="/caregiver_dashboard">

<button
style="
padding:15px;
width:220px;">

⬅ {TEXT("back")}

</button>

</a>

<br><br>

<a href="/delete_patient/{patient_id}"
onclick="return confirm('{TEXT("delete_confirm")}')">

<button
style="
background:red;
color:white;
padding:12px 20px;
border:none;
border-radius:8px;
font-size:16px;
cursor:pointer;">

🗑 {TEXT("delete_patient")}

</button>

</a>

</body>

</html>

"""

'''@app.route('/chatbot')
def chatbot():

    if 'user' not in session:
        return redirect('/login')

    return render_template(
        "chatbot.html",
        lang=session.get("language", "en"),
        translate=translate_text
    )'''

@app.route('/chatbot')
def chatbot():

    if 'user' not in session:
        return redirect('/login')

    response = request.args.get("response", "")

    return render_template(
        "chatbot.html",
        lang=session.get("language", "en"),
        translate=translate_text,
        response=response
    )

import re

def prepare_for_speech(answer, question):

    q = question.lower()

    speech = answer

    # ------------------------------------
    # Medicine Count
    # ------------------------------------

    if "total medicines stored" in answer.lower():

        number = re.findall(r"\d+", answer)

        if number:

            speech = f"You currently have {number[0]} medicines in your records."

    # ------------------------------------
    # Next Reminder
    # ------------------------------------

    elif "your next medicine is" in answer.lower():

        speech = answer

        speech = speech.replace("09:00", "9 AM")
        speech = speech.replace("10:00", "10 AM")
        speech = speech.replace("11:00", "11 AM")
        speech = speech.replace("20:30", "8:30 PM")
        speech = speech.replace("21:00", "9 PM")

    # ------------------------------------
    # Reminder List
    # ------------------------------------

    elif "💊" in answer or "🍽" in answer:

        medicine_count = answer.count("💊")

        meal_count = answer.count("🍽")

        speech = (

            f"You have {medicine_count} medicine reminders "

            f"and {meal_count} meal reminders scheduled today. "

            f"The complete reminder list is displayed on your screen."

        )

    # ------------------------------------
    # Medicine Details
    # ------------------------------------

    elif "Medicine :" in answer:

        speech = answer.replace("<br>", ". ")

    return speech

@app.route("/voice_command")
def voice_command():

    if "user" not in session:
        return redirect("/login")

    lang = session.get("language", "en")

    # ------------------------------------
    # Listen from Microphone
    # ------------------------------------

    command = listen_command(lang)

    print("Voice Command :", command)

    if not command:

        message = translate_text(
            "Sorry, I could not understand your voice."
        )

        speak_text(message, lang)

        return redirect("/chatbot")

    # ------------------------------------
    # Convert Question to English
    # (Only for processing)
    # ------------------------------------

    english_command = command

    if lang != "en":

        try:

            english_command = GoogleTranslator(
                source="auto",
                target="en"
            ).translate(command)

        except Exception:

            english_command = command

    print("English Command :", english_command)

    # ------------------------------------
    # Navigation Commands
    # ------------------------------------

    page = execute_command(english_command)
    print("PAGE =", page)

    if page:

        '''messages = {

            "en":"Opening requested page.",

            "kn":"ಬೇಡಿಕೆಯ ಪುಟವನ್ನು ತೆರೆಯಲಾಗುತ್ತಿದೆ.",

            "hi":"अनुरोधित पृष्ठ खोला जा रहा है।",

            "ta":"கோரப்பட்ட பக்கம் திறக்கப்படுகிறது.",

            "te":"అభ్యర్థించిన పేజీ తెరవబడుతోంది."

        }

        speak_text(messages.get(lang), lang)

        return redirect(page)'''

        print("REDIRECTING TO:", page)

        return redirect(page)

    # ------------------------------------
    # Healthcare Questions
    # ------------------------------------

    answer = process_question(english_command)

    print("ANSWER =", answer)

    # ------------------------------------
    # Translate Answer Back
    # ------------------------------------

    if lang != "en":

        answer = translate_text(answer)

    clean_answer = (
        answer
        .replace("<br>", " ")
        .replace("<br/>", " ")
        .replace("<br />", " ")
    )

    speech_answer = prepare_for_speech(clean_answer, english_command)

    print("Speech :", speech_answer)

    print("TYPE :", type(clean_answer))
    print("TEXT :", repr(clean_answer))

    speak_text(speech_answer, lang)

    #print("AFTER SPEAK")

    #print(clean_answer)

    # ------------------------------------
    # Speak Answer
    # ------------------------------------

    #speak_text(clean_answer, lang)
    #speak_text("Your next reminder is at nine o clock.", lang)

    from urllib.parse import quote

    return redirect(
    "/chatbot?response=" + quote(answer)
)

INTENTS = {

    "medicine_count": [

        "how many medicines",
        "medicine count",
        "medicine total",
        "total medicines",
        "number of medicines",
        "how many tablets",
        "how many drugs"

    ],

    "medicine_list": [

        "show medicines",
        "list medicines",
        "my medicines",
        "medicine list",
        "what medicines do i have",
        "show my medicines"

    ],

    "next_reminder": [

        "next reminder",
        "next medicine",
        "upcoming reminder",
        "upcoming medicine",
        "what is  next reminder",
        "what is  next medicine",
        "what should i take next"

    ],

    "reminder_list": [

        "show reminders",
        "my reminders",
        "reminder schedule",
        "today reminders",
        "today's reminders",
        "all reminders",
        "list reminders"

    ],

    "pending": [

        "pending medicine",
        "pending medicines",
        "which medicine is pending",
        "medicines left"

    ],

    "taken": [

        "taken medicines",
        "completed medicines",
        "which medicines did i take",
        "medicines taken"

    ],

    "medicine_list": [

    "show my medicines",
    "show medicines",
    "my medicines",
    "medicine list",
    "list my medicines",
    "what medicines do i have",
    "display medicines",

    # Kannada
    "ನನ್ನ ಔಷಧಗಳು",
    "ಔಷಧಗಳ ಪಟ್ಟಿ",
    "ಔಷಧಗಳನ್ನು ತೋರಿಸು",

    # Hindi
    "मेरी दवाइयाँ",
    "दवाइयों की सूची",
    "दवाइयाँ दिखाओ",

    # Tamil
    "என் மருந்துகள்",
    "மருந்து பட்டியல்",
    "மருந்துகளை காட்டு",

    # Telugu
    "నా మందులు",
    "మందుల జాబితా",
    "మందులు చూపించు"

],

}

'''def process_question(question):

    question = question.lower().strip()

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    patient_id = session.get("patient_id")

    answer = None

    # =====================================================
    # ALL REMINDERS
    # =====================================================

    if any(x in question for x in INTENTS["reminder_list"]):

        cursor.execute("""
        SELECT
            reminder_time,
            reminder_type,
            medicine,
            meal
        FROM reminders
        WHERE patient_id=?
        ORDER BY reminder_time
        """,(patient_id,))

        data = cursor.fetchall()

        if not data:

            answer = "No reminders available."

        else:

            answer = ""

            for time,rtype,medicine,meal in data:

                if rtype=="Meal":

                    answer += f"🍽 {meal} - {time}<br>"

                else:

                    answer += f"💊 {medicine} - {time}<br>"

    # =====================================================
    # MEDICINE COUNT
    # =====================================================

    elif any(x in question for x in INTENTS["medicine_count"]):

        cursor.execute("""

        SELECT COUNT(*)

        FROM medicines

        WHERE patient_id=?

        """,(patient_id,))

        count = cursor.fetchone()[0]

        answer = f"Total medicines stored: {count}"

    # =====================================================
    # NEXT REMINDER
    # =====================================================

    elif any(x in question for x in INTENTS["next_reminder"]):

        cursor.execute("""

        SELECT

            reminder_time,

            reminder_type,

            medicine,

            meal

        FROM reminders

        WHERE patient_id=?

        AND status='Pending'

        ORDER BY reminder_time

        LIMIT 1

        """,(patient_id,))

        row = cursor.fetchone()

        if row:

            time,rtype,medicine,meal = row

            if rtype=="Meal":

                answer = f"Your next reminder is {meal} at {time}"

            else:

                answer = f"Your next medicine is {medicine} at {time}"

        else:

            answer = "No pending reminders."

    # =====================================================
    # MEDICINE DETAILS
    # =====================================================

    else:

        cursor.execute("""

        SELECT

            medicine,

            dose,

            frequency,

            instruction,

            duration

        FROM medicines

        WHERE patient_id=?

        """,(patient_id,))

        medicines = cursor.fetchall()

        for med,dose,freq,instr,dur in medicines:

            if med.lower() in question:

                answer=f"""
Medicine : {med}<br>
Dose : {dose}<br>
Frequency : {freq}<br>
Instruction : {instr}<br>
Duration : {dur}
"""

                break

        if answer is None:

            answer="""
Sorry, I couldn't understand your question.<br><br>

You can ask things like:<br>

• How many medicines do I have?<br>
• What is my next reminder?<br>
• Show my reminders<br>
• Tell me about Dolo 650<br>
• Tell me about Glycomet<br>
"""

    conn.close()

    return answer

@app.route('/ask', methods=['POST'])
def ask():

    question = request.form["question"]

    answer = process_question(question)

    lang = session.get("language","en")

    if lang != "en":

        answer = translate_text(answer)

    title = {
        "en":"🤖 SmartMed Response",
        "kn":"🤖 SmartMed ಉತ್ತರ",
        "hi":"🤖 SmartMed उत्तर",
        "ta":"🤖 SmartMed பதில்",
        "te":"🤖 SmartMed సమాధానం"
    }

    button = {
        "en":"Ask Another Question",
        "kn":"ಇನ್ನೊಂದು ಪ್ರಶ್ನೆ ಕೇಳಿ",
        "hi":"एक और प्रश्न पूछें",
        "ta":"மற்றொரு கேள்வி கேளுங்கள்",
        "te":"మరో ప్రశ్న అడగండి"
    }

    return f"""
<div style="
max-width:800px;
margin:40px auto;
padding:30px;
background:white;
border-radius:15px;
box-shadow:0 4px 15px rgba(0,0,0,.15);
font-family:Segoe UI;
">

<h2 style="color:#2563eb;">
{title.get(lang,title["en"])}
</h2>

<hr>

<div style="
font-size:18px;
line-height:1.8;
">

{answer}

</div>

<br><br>

<a href="/chatbot">

<button style="
background:#2563eb;
color:white;
padding:12px 20px;
border:none;
border-radius:8px;
font-size:16px;
cursor:pointer;
">

{button.get(lang,button["en"])}

</button>

</a>

</div>
"""'''
def process_question(question):

    question = question.lower().strip()

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    patient_id = session.get("patient_id")

    answer = None

    # =====================================================
    # ALL REMINDERS
    # =====================================================

    if any(x in question for x in INTENTS["reminder_list"]):

        cursor.execute("""
        SELECT
            reminder_time,
            reminder_type,
            medicine,
            meal
        FROM reminders
        WHERE patient_id=?
        ORDER BY reminder_time
        """, (patient_id,))

        data = cursor.fetchall()

        if not data:

            answer = "No reminders available."

        else:

            answer = ""

            for time, rtype, medicine, meal in data:

                if rtype == "Meal":

                    answer += f"🍽 {meal} - {time}<br>"

                else:

                    answer += f"💊 {medicine} - {time}<br>"

    # =====================================================
    # SHOW MY MEDICINES
    # =====================================================

    elif any(x in question for x in INTENTS["medicine_list"]):

        cursor.execute("""
        SELECT
            medicine,
            dose
        FROM medicines
        WHERE patient_id=?
        ORDER BY medicine
        """, (patient_id,))

        medicines = cursor.fetchall()

        if not medicines:

            answer = "No medicines found."

        else:

            answer = ""

            for med, dose in medicines:

                answer += f"💊 {med} ({dose})<br>"

    # =====================================================
    # MEDICINE COUNT
    # =====================================================

    elif any(x in question for x in INTENTS["medicine_count"]):

        cursor.execute("""

        SELECT COUNT(*)

        FROM medicines

        WHERE patient_id=?

        """, (patient_id,))

        count = cursor.fetchone()[0]

        answer = f"Total medicines stored: {count}"

    # =====================================================
    # NEXT REMINDER
    # =====================================================

    elif any(x in question for x in INTENTS["next_reminder"]):

        cursor.execute("""

        SELECT

            reminder_time,

            reminder_type,

            medicine,

            meal

        FROM reminders

        WHERE patient_id=?

        AND status='Pending'

        ORDER BY reminder_time

        LIMIT 1

        """, (patient_id,))

        row = cursor.fetchone()

        if row:

            time, rtype, medicine, meal = row

            if rtype == "Meal":

                answer = f"Your next reminder is {meal} at {time}"

            else:

                answer = f"Your next medicine is {medicine} at {time}"

        else:

            answer = "No pending reminders."

    # =====================================================
    # MEDICINE DETAILS
    # =====================================================

    else:

        cursor.execute("""

        SELECT

            medicine,

            dose,

            frequency,

            instruction,

            duration

        FROM medicines

        WHERE patient_id=?

        """, (patient_id,))

        medicines = cursor.fetchall()

        for med, dose, freq, instr, dur in medicines:

            if med.lower() in question:

                answer = f"""
Medicine : {med}<br>
Dose : {dose}<br>
Frequency : {freq}<br>
Instruction : {instr}<br>
Duration : {dur}
"""

                break

        if answer is None:

            answer = """
Sorry, I couldn't understand your question.<br><br>

You can ask things like:<br><br>

• Show my medicines<br>
• How many medicines do I have?<br>
• What is my next reminder?<br>
• Show my reminders<br>
• Tell me about Dolo 650<br>
• Tell me about Glycomet<br>
"""

    conn.close()

    return answer

'''@app.route('/ask', methods=['POST'])
def ask():

    question = request.form['question'].lower()

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    if "reminder" in question:

        patient_id = session.get("patient_id")

        cursor.execute("""
    SELECT
        reminder_time,
        reminder_type,
        medicine,
        meal
    FROM reminders
    WHERE patient_id=?
    ORDER BY reminder_time
    """, (patient_id,))

        data = cursor.fetchall()

        answer = ""

        for time, rtype, medicine, meal in data:

           if rtype == "Meal":

            answer += f"🍽 {meal} - {time}<br>"

           else:

            answer += f"💊 {medicine} - {time}<br>"
    elif "how many medicines" in question:

        patient_id = session.get("patient_id")

        cursor.execute(
            """SELECT COUNT(*) 
            FROM medicines
            WHERE patient_id=? 
            """ ,(patient_id,))
        

        count = cursor.fetchone()[0]

        answer = f"Total medicines stored: {count}"

    elif "next reminder" in question or "next medicine" in question:

        patient_id = session.get("patient_id")

        cursor.execute("""
    SELECT
        reminder_time,
        reminder_type,
        medicine,
        meal
    FROM reminders
    WHERE patient_id=?
    AND status='Pending'
    ORDER BY reminder_time
    LIMIT 1
    """, (patient_id,))

        row = cursor.fetchone()

        if row:

           time, rtype, medicine, meal = row

           if rtype == "Meal":

              answer = f"Your next reminder is {meal} at {time}"

           else:

            answer = f"Your next medicine is {medicine} at {time}"

        else:

            answer = "No pending reminders."

    else:

        patient_id = session.get("patient_id")

        cursor.execute("""
    SELECT
        medicine,
        dose,
        frequency,
        instruction,
        duration
    FROM medicines
    WHERE patient_id=?
    """, (patient_id,))

        medicines = cursor.fetchall()

        answer = None

        for med, dose, freq, instr, dur in medicines:

           if med.lower() in question:

            answer = f"""
Medicine : {med}<br>
Dose : {dose}<br>
Frequency : {freq}<br>
Instruction : {instr}<br>
Duration : {dur}
"""

            break

        if answer is None:

          answer = "Sorry, I don't know that yet."

   

    conn.close()
    lang = session.get("language","en")

    if lang != "en":
    
       answer = translate_text(answer)

    

    title = {
    "en": "🤖 SmartMed Response",
    "kn": "🤖 SmartMed ಉತ್ತರ",
    "hi": "🤖 SmartMed उत्तर",
    "ta": "🤖 SmartMed பதில்",
    "te": "🤖 SmartMed సమాధానం"
}

    button = {
    "en": "Ask Another Question",
    "kn": "ಇನ್ನೊಂದು ಪ್ರಶ್ನೆ ಕೇಳಿ",
    "hi": "एक और प्रश्न पूछें",
    "ta": "மற்றொரு கேள்வி கேளுங்கள்",
    "te": "మరో ప్రశ్న అడగండి"
}

    return f"""
<div style="
max-width:800px;
margin:40px auto;
padding:30px;
background:white;
border-radius:15px;
box-shadow:0 4px 15px rgba(0,0,0,.15);
font-family:Segoe UI;
">

<h2 style="color:#2563eb;">
{title.get(lang, title["en"])}
</h2>

<hr>

<div style="
font-size:18px;
line-height:1.8;
">

{answer}

</div>

<br><br>

<a href="/chatbot">

<button style="
background:#2563eb;
color:white;
padding:12px 20px;
border:none;
border-radius:8px;
font-size:16px;
cursor:pointer;">

{button.get(lang, button["en"])}

</button>

</a>

</div>
"""  '''
    

@app.route('/my_reminders')
def my_reminders():

    patient_id = session.get("patient_id")

    if patient_id is None:
        return redirect(url_for("login"))

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            reminder_time,
            reminder_type,
            medicine,
            meal,
            status
        FROM reminders
        WHERE patient_id=?
        ORDER BY reminder_time
    """, (patient_id,))

    reminders = cursor.fetchall()

    conn.close()

    html = """
    <html>

    <body style="font-family:Segoe UI;background:#eef2ff;">

    <div style="
        width:850px;
        margin:30px auto;
        background:white;
        padding:25px;
        border-radius:15px;
        box-shadow:0px 5px 20px rgba(0,0,0,0.2);
    ">

    <h1 style="text-align:center;color:#2563eb;">
        🔔 My AI Reminders
    </h1>

    <table border="1"
           cellpadding="10"
           style="width:100%;
                  border-collapse:collapse;
                  text-align:center;">

    <tr style="background:#dbeafe;">
        <th>Time</th>
        <th>Type</th>
        <th>Reminder</th>
        <th>Status</th>
    </tr>
    """

    for time, rtype, medicine, meal, status in reminders:

        if status == "Taken":
            status_html = "<span style='color:green;'>✅ Taken</span>"
        else:
            status_html = "<span style='color:red;'>⏳ Pending</span>"

        if rtype == "Meal":
            reminder = f"🍽 {meal}"
            type_html = "🍽 Meal"
        else:
            reminder = f"💊 {medicine}"
            type_html = "💊 Medicine"

        html += f"""
        <tr>
            <td>{time}</td>
            <td>{type_html}</td>
            <td>{reminder}</td>
            <td>{status_html}</td>
        </tr>
        """

    html += """
    </table>

    <br><br>

    <a href="/chatbot">
        <button style="
            padding:12px 25px;
            background:#2563eb;
            color:white;
            border:none;
            border-radius:8px;
            cursor:pointer;
        ">
        ⬅ Back to Chatbot
        </button>
    </a>

    </div>

    </body>
    </html>
    """

    return html
@app.route('/emergency_contact')
def emergency_contact():

    lang = session.get("language", "en")

    title = (
        "ತುರ್ತು ಸಂಪರ್ಕ" if lang=="kn"
        else "आपातकालीन संपर्क" if lang=="hi"
        else "அவசர தொடர்பு" if lang=="ta"
        else "అత్యవసర సంప్రదింపు" if lang=="te"
        else "Emergency Contact"
    )

    member = (
        "ಕುಟುಂಬದ ಸದಸ್ಯ" if lang=="kn"
        else "परिवार का सदस्य" if lang=="hi"
        else "குடும்ப உறுப்பினர்" if lang=="ta"
        else "కుటుంబ సభ్యుడు" if lang=="te"
        else "Family Member"
    )

    call = (
        "ಈಗ ಕರೆ ಮಾಡಿ" if lang=="kn"
        else "अभी कॉल करें" if lang=="hi"
        else "இப்போது அழைக்கவும்" if lang=="ta"
        else "ఇప్పుడే కాల్ చేయండి" if lang=="te"
        else "Call Now"
    )

    back = (
        "ಹಿಂದೆ" if lang=="kn"
        else "वापस" if lang=="hi"
        else "திரும்பு" if lang=="ta"
        else "వెనుకకు" if lang=="te"
        else "Back"
    )

    return f"""
    <div style='width:600px;
                margin:auto;
                text-align:center;
                padding:30px;'>

    <h1>🚨 {title}</h1>

    <h2>{member}</h2>

    <h3>+91 9483288340</h3>

    <br>

    <a href='tel:+919483288340'>
    <button style='background:green;
                   color:white;
                   padding:15px;
                   font-size:18px;
                   border:none;
                   border-radius:10px;'>

    📞 {call}

    </button>
    </a>

    <br><br>

    <a href='/chatbot'>
    <button>⬅ {back}</button>
    </a>

    </div>
    """

@app.route('/my_medicines')
def my_medicines():

    patient_id = session.get("patient_id")

    if patient_id is None:
        return redirect(url_for("login"))

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT medicine
    FROM medicines
    WHERE patient_id=?
    """, (patient_id,))

    data = cursor.fetchall()

    conn.close()

    lang = session.get("language", "en")

    title = (
        "ನನ್ನ ಔಷಧಿಗಳು" if lang=="kn"
        else "मेरी दवाइयाँ" if lang=="hi"
        else "என் மருந்துகள்" if lang=="ta"
        else "నా మందులు" if lang=="te"
        else "My Medicines"
    )

    back = (
        "ಹಿಂದೆ" if lang=="kn"
        else "वापस" if lang=="hi"
        else "திரும்பு" if lang=="ta"
        else "వెనుకకు" if lang=="te"
        else "Back"
    )

    html = f"""
    <html>

    <body style='font-family:Segoe UI;background:#eef2ff;'>

    <div style='width:700px;
                margin:30px auto;
                background:white;
                padding:20px;
                border-radius:15px;
                box-shadow:0px 5px 20px rgba(0,0,0,0.2);'>

    <h1>💊 {title}</h1>
    """

    for row in data:

        html += f"""

        <div style='background:#dbeafe;
                    padding:15px;
                    margin:10px;
                    border-radius:10px;'>

            <h3>{row[0]}</h3>

        </div>

        """

    html += f"""

    <a href='/chatbot'>
        <button>{back}</button>
    </a>

    </div>

    </body>

    </html>

    """

    return html

@app.route('/next_medicine')
def next_medicine():

    patient_id = session.get("patient_id")

    if patient_id is None:
        return redirect(url_for("login"))

    lang = session.get("language", "en")

    language_codes = {
        "en": "en-US",
        "kn": "kn-IN",
        "hi": "hi-IN",
        "ta": "ta-IN",
        "te": "te-IN"
    }

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        reminder_time,
        reminder_type,
        medicine,
        meal
    FROM reminders
    WHERE patient_id=?
    AND status='Pending'
    ORDER BY reminder_time
    LIMIT 1
    """, (patient_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:

        return f"""
        <html>
        <body>

        <h1>⏰ {TEXT("next_reminder")}</h1>

        <h2>{translate_text("No pending reminders.")}</h2>

        <a href="/chatbot">
        <button>{TEXT("back")}</button>
        </a>

        </body>
        </html>
        """

    reminder_time, reminder_type, medicine, meal = row

    # ----------------------------------
    # Display title
    # ----------------------------------

    if reminder_type == "Meal":

        title = f"🍽 {meal}"

    else:

        title = f"💊 {medicine}"

    # ----------------------------------
    # Voice reminder
    # ----------------------------------

    if reminder_type == "Meal":

       speech_text = VOICE_MESSAGES[lang]["meal"].format(
        meal=meal
    )

    else:

       speech_text = VOICE_MESSAGES[lang]["medicine"].format(
        medicine=medicine
    )

    print("Speech Text =", speech_text)

    return f"""
    <html>

    <body>

    <h1>⏰ {TEXT("next_reminder")}</h1>

    <h2>{title}</h2>

    <h3>{TEXT("time")}: {reminder_time}</h3>

    <button onclick="speakReminder()">
        🔊 {TEXT("read_aloud")}
    </button>

    
    <script>

    function speakReminder() {{

        let speech = new SpeechSynthesisUtterance(
            `{speech_text}`
        );

        speech.lang = "{language_codes.get(lang,'en-US')}";

        window.speechSynthesis.speak(speech);

    }}

    </script>
    
    


    <br><br>

    <a href="/chatbot">
        <button>{TEXT("back")}</button>
    </a>

    </body>

    </html>
    """

@app.route('/mark_taken/<int:id>')
def mark_taken(id):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    current_time = datetime.now().strftime(
        "%d-%b-%Y %I:%M %p"
    )

    cursor.execute(
        """
        UPDATE medicines
        SET taken='Taken',
            taken_time=?
        WHERE id=?
        """,
        (current_time, id)
    )

    conn.commit()
    conn.close()

    lang = session.get("language", "en")

    return f"""

    <h2>

    ✅ {
    "ಔಷಧವನ್ನು ತೆಗೆದುಕೊಂಡಂತೆ ಗುರುತಿಸಲಾಗಿದೆ" if lang=="kn"
    else "दवा ली गई के रूप में चिह्नित" if lang=="hi"
    else "மருந்து எடுத்ததாக குறிக்கப்பட்டது" if lang=="ta"
    else "ఔషధం తీసుకున్నట్లు గుర్తించబడింది" if lang=="te"
    else "Medicine Marked as Taken"
    }

    </h2>

    <a href="/view">

    {
    "ದಾಖಲೆಗಳಿಗೆ ಹಿಂತಿರುಗಿ" if lang=="kn"
    else "रिकॉर्ड पर वापस जाएँ" if lang=="hi"
    else "பதிவுகளுக்கு திரும்பு" if lang=="ta"
    else "రికార్డులకు తిరిగి వెళ్ళండి" if lang=="te"
    else "Back to Records"
    }

    </a>

    """

@app.route('/mark_reminder_taken/<int:reminder_id>')
def mark_reminder_taken(reminder_id):

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    current_time = datetime.now().strftime(
        "%d-%b-%Y %I:%M %p"
    )

    # ---------------------------------
    # Get reminder details
    # ---------------------------------

    cursor.execute("""
    SELECT
        patient_id,
        medicine
    FROM reminders
    WHERE id=?
    """, (reminder_id,))

    row = cursor.fetchone()

    if row is None:

        conn.close()

        return "Reminder not found."

    patient_id = row[0]
    medicine = row[1]

    # ---------------------------------
    # Mark this reminder as Done
    # ---------------------------------

    cursor.execute("""
    UPDATE reminders

    SET status='Done'

    WHERE id=?
    """, (reminder_id,))

    # ---------------------------------
    # Are there any Pending reminders
    # for this medicine?
    # ---------------------------------

    cursor.execute("""
    SELECT COUNT(*)

    FROM reminders

    WHERE
        patient_id=?
        AND medicine=?
        AND reminder_type='Medicine'
        AND status='Pending'
    """,
    (
        patient_id,
        medicine
    ))

    pending = cursor.fetchone()[0]

    # ---------------------------------
    # If all reminders are Done,
    # mark medicine Taken
    # ---------------------------------

    if pending == 0:

        cursor.execute("""
        UPDATE medicines

        SET
            taken='Taken',
            taken_time=?

        WHERE
            patient_id=?
            AND medicine=?
        """,
        (
            current_time,
            patient_id,
            medicine
        ))

    conn.commit()
    conn.close()

    return redirect("/reminders")

@app.route('/add_patient')
def add_patient():

    if 'user' not in session:
        return redirect('/login')

    return render_template("add_patient.html",lang=session.get("language","en"))
@app.route('/save_patient', methods=['POST'])
def save_patient():

    photo = request.files['photo']

    photo.save("static/" + photo.filename)

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients
    (
        caregiver_username,
        patient_name,
        age,
        photo,
        phone,
        address,
        blood
    )

    VALUES(?,?,?,?,?,?,?)
    """, (

        session['user'],

        request.form['name'],

        request.form['age'],

        photo.filename,

        request.form['phone'],

        request.form['address'],

        request.form['blood']

    ))

    conn.commit()

    conn.close()

    return redirect('/caregiver_dashboard')

@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect("medicine.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (patient_id,)
    )

    conn.commit()
    conn.close()

    session.pop('patient_id', None)
    session.pop('patient_name', None)

    return redirect('/caregiver_dashboard')

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        
    )

