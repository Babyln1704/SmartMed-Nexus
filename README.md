# 🏥 SmartMed Nexus

**SmartMed Nexus** is an integrated multilingual healthcare assistant designed to simplify medicine management for caregivers and elderly patients. The platform combines AI-powered prescription OCR, drug interaction analysis, multilingual voice assistance, medicine reminders, and adherence tracking into a single healthcare solution.

---

## 📌 Features

### 📷 AI-Powered Prescription OCR
- Extracts medicine names from prescription images.
- Reduces manual data entry.
- Supports digital prescription management.

### 💊 Drug Interaction Detection
- Identifies potential interactions between prescribed medicines.
- Uses the TWOSIDES drug interaction dataset.
- Helps improve medication safety.

### 🔔 Smart Medicine & Meal Reminders
- Medicine reminders
- Meal reminders
- Missed dose tracking
- Reminder history

### 🎤 Multilingual Voice Assistant
Supports voice interaction in:
- English
- Kannada
- Hindi
- Tamil
- Telugu

Users can navigate the application and ask healthcare-related questions using voice commands.

### 🤖 AI Healthcare Chatbot
Provides answers to healthcare-related queries such as:
- Medicine information
- Reminder details
- Patient medicine list
- Next scheduled reminder

### 👨‍⚕️ Caregiver Dashboard
- Patient management
- Medicine management
- Reminder management
- Adherence monitoring

### 📈 Medicine Adherence Tracking
Tracks:
- Taken medicines
- Pending medicines
- Overall adherence percentage

### 🚨 Emergency Contact Support
Stores emergency contacts for quick access during emergencies.

---

# AI Technologies Used

SmartMed Nexus integrates Artificial Intelligence in multiple components:

- AI-based Prescription OCR
- Speech Recognition
- Natural Language Processing (NLP)
- Multilingual Language Translation

---

# Technologies Used

## Backend
- Python
- Flask

## Database
- SQLite

## AI & Libraries
- PaddleOCR
- OpenCV
- SpeechRecognition
- pyttsx3
- Deep Translator
- Pandas
- NumPy
- RapidFuzz

---

# Project Structure

```
SmartMed-Nexus/
│
├── app.py
├── medicine_parser.py
├── interaction_service.py
├── templates/
├── static/
├── uploads/
├── screenshots/
├── indian_brands.csv
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/spc-dpc/Smartmed-AI.git
```

## Move into Project

```bash
cd Smartmed-AI
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

The application will be available at:

```
http://127.0.0.1:5000
```

---

# Screenshots

Add screenshots of:

- Login Page
- Caregiver Dashboard
- Prescription OCR
- Drug Interaction Detection
- Medicine Reminder
- Voice Assistant
- AI Chatbot

---

# Future Scope

- IoT-enabled Smart Medicine Box for automatic medicine dispensing and real-time adherence monitoring.
- Smartwatch integration for health monitoring.
- Cloud database synchronization.
- Secure role-based authentication.
- Machine Learning-based adherence prediction.
- Personalized reminder optimization.
- Hospital Information System integration.

---

# Datasets Used

- Indian Medicine Brand Dataset
- TWOSIDES Drug Interaction Dataset

---

# Limitations

- OCR accuracy depends on prescription image quality.
- Adherence is currently caregiver-confirmed rather than automatically verified.
- Multilingual speech output depends on the availability of system voices.
- The chatbot is limited to healthcare-specific predefined intents.

---

# Authors

**Shailaja P C**

Department of Artificial Intelligence & Machine Learning

PES University

---

# License

This project is developed for educational and research purposes.
