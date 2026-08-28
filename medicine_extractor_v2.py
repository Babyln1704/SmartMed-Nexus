import re
import pandas as pd
from medical_ai_detector import detect_candidates_ai
from rapidfuzz import process, fuzz

print("Loading SmartMed AI Medicine Extractor V2...")

# -------------------------------
# Indian Brand Database
# -------------------------------

INDIAN_BRANDS = pd.read_csv("indian_brands.csv")

INDIAN_BRANDS.rename(columns={
    "brand_name": "brand",
    "generic_name": "generic"
}, inplace=True)

INDIAN_BRANDS["brand"] = INDIAN_BRANDS["brand"].str.lower()
INDIAN_BRANDS["generic"] = INDIAN_BRANDS["generic"].str.lower()

BRAND_TO_GENERIC = dict(
    zip(
        INDIAN_BRANDS["brand"],
        INDIAN_BRANDS["generic"]
    )
)

# -------------------------------
# TWOSIDES
# -------------------------------

TWOSIDES = pd.read_parquet("twosides.parquet")

TWOSIDES["drug_1"] = TWOSIDES["drug_1"].str.lower()
TWOSIDES["drug_2"] = TWOSIDES["drug_2"].str.lower()

TWOSIDES_DRUGS = sorted(
    set(TWOSIDES["drug_1"]).union(
        set(TWOSIDES["drug_2"])
    )
)

INDIAN_BRANDS_LIST = sorted(
    BRAND_TO_GENERIC.keys()
)

#print("Indian Brands :", len(INDIAN_BRANDS_LIST))
#print("TWOSIDES Drugs:", len(TWOSIDES_DRUGS))
print("Indian Brands :", len(INDIAN_BRANDS_LIST))
print("TWOSIDES Drugs:", len(TWOSIDES_DRUGS))

# ------------------------------------
# Medical Synonyms
# Used ONLY for searching.
# Original medicine name is preserved.
# ------------------------------------

MEDICAL_SYNONYMS = {

    # Pain / Fever
    "paracetamol": "acetaminophen",
    "acetaminophen": "acetaminophen",

    # Asthma
    "salbutamol": "albuterol",
    "albuterol": "albuterol",

    # Emergency
    "adrenaline": "epinephrine",
    "epinephrine": "epinephrine",

    # Local Anaesthetic
    "lignocaine": "lidocaine",
    "lidocaine": "lidocaine",

    # Diuretic
    "frusemide": "furosemide",
    "furosemide": "furosemide",

    # Diabetes
    "glyburide": "glibenclamide",
    "glibenclamide": "glibenclamide",

    # Emergency
    "noradrenaline": "norepinephrine",
    "norepinephrine": "norepinephrine",

    # Bronchodilator
    "isoprenaline": "isoproterenol",
    "isoproterenol": "isoproterenol",

    # Antispasmodic
    "hyoscine": "scopolamine",
    "scopolamine": "scopolamine",

    # Vitamins
    "vitamin b9": "folic acid",
    "folic acid": "folic acid"

}

import re

def normalize_search_name(name):
    """
    Normalize medicine name before searching.

    Examples
    --------
    Paracetamol 500 Tablet
        ↓
    acetaminophen

    Cetirizine 10 mg
        ↓
    cetirizine

    Dolo 650
        ↓
    dolo 650
    """

    name = name.lower().strip()

    # -----------------------------
    # Remove dosage units
    # -----------------------------

    name = re.sub(
        r"\b\d+\s*(mg|mcg|g|ml)\b",
        "",
        name
    )

    # -----------------------------
    # Remove medicine forms
    # -----------------------------

    name = re.sub(
        r"\b(tablet|tab|capsule|cap|syrup|injection|inj)\b",
        "",
        name
    )

    # -----------------------------
    # Collapse multiple spaces
    # -----------------------------

    name = " ".join(name.split())

    # -----------------------------
    # Remove trailing strength
    #
    # Example:
    # Paracetamol 500
    #        ↓
    # Paracetamol
    #
    # Dolo 650
    #        ↓
    # Keep (brand medicine)
    # -----------------------------

    words = name.split()

    if len(words) >= 2:

        last = words[-1]

        if last.isdigit():

            # Brand medicines where strength
            # is part of the name
            keep_strength = {

                "dolo",
                "pan",
                "crocin",
                "calpol",
                "ecosprin",
                "glycomet"

            }

            if words[0] not in keep_strength:

                name = " ".join(words[:-1])

    # -----------------------------
    # Medical Synonyms
    # -----------------------------

    name = MEDICAL_SYNONYMS.get(
        name,
        name
    )

    return name






# ==========================================
# WORDS TO IGNORE
# ==========================================

STOP_WORDS = {

    # Common words
    "tablet","tab","tabs",
    "capsule","cap","caps",

    "take","after","before",
    "food","morning","night",
    "daily","twice","once",

    "doctor","dr","hospital",
    "clinic","patient",
    "name","age","gender",
    "diagnosis",
    "complaints",
    "advice",
    "registration",

    "mg","ml",

    "days","day",

    "follow","review",

    "male","female",

    "years","year"
}

# ==========================================
# CLEAN OCR TEXT
# ==========================================

# ==========================================
# CLEAN OCR TEXT (Production V2.1)
# ==========================================

def clean_ocr_text(text):

    text = text.lower()

    # ----------------------------------
    # OCR Corrections
    # ----------------------------------

    replacements = {

        "daly": "daily",
        "dailv": "daily",

        "teblet": "tablet",
        "tabiet": "tablet",
        "tahlet": "tablet",

        "capsuie": "capsule",

        "alter": "after",
        "afterr": "after",

        "befcre": "before",
        "bcfere": "before",

        "foad": "food",
        "fcod": "food",

        "dolo650": "dolo 650",
        "pan40": "pan 40",
        "glycomet500": "glycomet 500"
    }

    for wrong, correct in replacements.items():

        text = text.replace(wrong, correct)

    # ----------------------------------
    # Remove punctuation
    # ----------------------------------

    text = re.sub(r"[-_/]", " ", text)

    text = re.sub(r"[^\w\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ==========================================
# OCR ERROR CORRECTION
# ==========================================

def correct_ocr_errors(text):

    corrections = {

        # Common OCR mistakes
        "dola": "dolo",
        "660": "650",

        "a0": "40",

        "teblet": "tablet",
        "tabiet": "tablet",
        "tahlet": "tablet",

        "capsuie": "capsule",

        "alter": "after",
        "bcfere": "before",

        "fieve": "zincovit",

        "glycomet500": "glycomet 500",
        "dolo650": "dolo 650",
        "pan40": "pan 40"
    }

    words = text.split()

    corrected = []

    for word in words:

        corrected.append(
            corrections.get(word, word)
        )

    return " ".join(corrected)



# ==========================================
# GENERATE SMART MEDICINE CANDIDATES
# Production V2.1
# ==========================================

def generate_candidates(text):

    words = text.split()

    candidates = set()

    # ----------------------------------
    # Ignore sections after
    # General Advice / Follow Up
    # ----------------------------------

    stop_sections = {

        "advice",
        "follow",
        "review",
        "signature",
        "registration",
        "doctor"
    }

    filtered = []

    stop = False

    for word in words:

        if word in stop_sections:
            stop = True

        if stop:
            continue

        if word in STOP_WORDS:
            continue

        filtered.append(word)

    # ----------------------------------
    # Build candidates
    # ----------------------------------

    for i in range(len(filtered)):

        # Single word

        if len(filtered[i]) > 2:

            candidates.add(filtered[i])

        # Two words

        if i + 1 < len(filtered):

            candidates.add(

                filtered[i]
                + " "
                + filtered[i + 1]

            )

        # Brand + Strength

        if (

            i + 1 < len(filtered)

            and filtered[i + 1].isdigit()

        ):

            candidates.add(

                filtered[i]
                + " "
                + filtered[i + 1]

            )

    return sorted(candidates)

# ==========================================
# AI RANKING SCORE
# ==========================================

def calculate_score(candidate, matched_name, fuzzy_score, source):

    score = fuzzy_score

    # Indian Brand Priority
    if source == "Indian Brand":
        score += 10

    # Number Matching
    candidate_numbers = re.findall(r"\d+", candidate)
    matched_numbers = re.findall(r"\d+", matched_name)

    if candidate_numbers and matched_numbers:
        if candidate_numbers == matched_numbers:
            score += 20

    # Common Word Bonus
    candidate_words = set(candidate.split())
    matched_words = set(matched_name.split())

    common = len(candidate_words.intersection(matched_words))

    score += common * 5
    # -----------------------------------
# Medicine Pattern Bonus
# WORD + NUMBER
# Example:
# Dolo 650
# PAN 40
# AZEE 500
# -----------------------------------

    candidate_has_number = bool(re.search(r"\d+", candidate))
    matched_has_number = bool(re.search(r"\d+", matched_name))

    if candidate_has_number and matched_has_number:
     score += 15

    return score

# ==========================================
# AI MEDICINE MATCHER
# ==========================================

'''def match_medicine(candidate):

    best = None

    # ----------------------------
    # Search Indian Brand Database
    # ----------------------------

    indian = process.extractOne(
        candidate,
        INDIAN_BRANDS_LIST,
        scorer=fuzz.WRatio
    )

    if indian:

        name, score, _ = indian

        if score >= 90:

            best = {
                "medicine": name,
                "generic": BRAND_TO_GENERIC.get(name, ""),
                "source": "Indian Brand",
                "confidence": round(score, 2)
            }

    # ----------------------------
    # Search TWOSIDES
    # ----------------------------

    twosides = process.extractOne(
        candidate,
        TWOSIDES_DRUGS,
        scorer=fuzz.WRatio
    )

    if twosides:

        name, score, _ = twosides

        if score >= 90:

            if best is None or score > best["confidence"]:

                best = {
                    "medicine": name,
                    "generic": name,
                    "source": "TWOSIDES",
                    "confidence": round(score, 2)
                }

    return best'''



# ==========================================
# EXTRACT ALL MEDICINES
# ==========================================
# ==========================================
# AI MEDICINE MATCHER
# Production V2.1
# ==========================================

def match_medicine(candidate):

    # ------------------------------------
# Preserve Original Medicine Name
# ------------------------------------

    original_candidate = candidate.strip().lower()

    if len(original_candidate) < 3:
      return None

# ------------------------------------
# Normalize Search Name
# ------------------------------------

    search_candidate = normalize_search_name(
    original_candidate
)

# ------------------------------------
# Candidate Validation
# ------------------------------------

    banned_words = {

    "water","drink","food","doctor",
    "hospital","clinic","patient",
    "diagnosis","advice","review",
    "follow","registration",
    "signature","male","female",
    "morning","night","daily",
    "tablet","capsule","mg","ml"

}

    words = original_candidate.split()

    if words and all(word in banned_words for word in words):
       return None

# ------------------------------------
# Exact Indian Brand Match
# ------------------------------------

    if search_candidate in BRAND_TO_GENERIC:

      return {

        "medicine": original_candidate,

        "generic": BRAND_TO_GENERIC[
            search_candidate
        ],

        "source": "Indian Brand",

        "confidence": 100.0,

        "ai_score": 155.0,

        "confidence_level": "High"

    }

# ------------------------------------
# Exact TWOSIDES Match
# ------------------------------------

    if search_candidate in TWOSIDES_DRUGS:

     return {

        "medicine": original_candidate,

        "generic": search_candidate,

        "source": "TWOSIDES",

        "confidence": 100.0,

        "ai_score": 155.0,

        "confidence_level": "High"

    }

# Continue fuzzy search using normalized name

    candidate = search_candidate
    
    

    all_results = []

    # ------------------------------------
    # Indian Brand Search
    # ------------------------------------

    indian_matches = process.extract(

        candidate,

        INDIAN_BRANDS_LIST,

        scorer=fuzz.WRatio,

        limit=5

    )

    for name, fuzzy_score, _ in indian_matches:

        # Reject weak matches immediately
        if fuzzy_score < 90:
            continue

        ai_score = calculate_score(

            candidate,

            name,

            fuzzy_score,

            "Indian Brand"

        )

        all_results.append({

            "medicine": name,

            "generic": BRAND_TO_GENERIC.get(name, ""),

            "source": "Indian Brand",

            "confidence": round(fuzzy_score,2),

            "ai_score": round(ai_score,2)

        })

    # ------------------------------------
    # TWOSIDES Search
    # ------------------------------------

    twosides_matches = process.extract(

        candidate,

        TWOSIDES_DRUGS,

        scorer=fuzz.WRatio,

        limit=5

    )

    for name, fuzzy_score, _ in twosides_matches:

        if fuzzy_score < 93:
            continue

        ai_score = calculate_score(

            candidate,

            name,

            fuzzy_score,

            "TWOSIDES"

        )

        all_results.append({

            "medicine": name,

            "generic": name,

            "source": "TWOSIDES",

            "confidence": round(fuzzy_score,2),

            "ai_score": round(ai_score,2)

        })

    if not all_results:
        return None

    # ------------------------------------
    # AI Ranking
    # ------------------------------------

    all_results.sort(

        key=lambda x: (

            x["ai_score"],

            x["confidence"]

        ),

        reverse=True

    )

    best = all_results[0]

    # ------------------------------------
    # Prefer Indian Brand
    # ------------------------------------

    for result in all_results:

        if result["source"] == "Indian Brand":

            if result["ai_score"] >= best["ai_score"] - 5:

                best = result

                break

    # ------------------------------------
    # Confidence Level
    # ------------------------------------

    if best["confidence"] >= 97:

        best["confidence_level"] = "High"

    elif best["confidence"] >= 93:

        best["confidence_level"] = "Medium"

    else:

        best["confidence_level"] = "Low"

    return best
# ==========================================
# EXTRACT MEDICINES V2
# ==========================================

def extract_medicines_v2(ocr_text):

    cleaned = clean_ocr_text(ocr_text)
    cleaned = correct_ocr_errors(cleaned)

    #candidates = generate_candidates(cleaned)
    candidates = detect_candidates_ai(ocr_text)
    print("\n========== AI CANDIDATES ==========")
    print(candidates)

    medicines = []

    for candidate in candidates:

        result = match_medicine(candidate)

        if result:
            medicines.append(result)

    # ---------------------------------------
    # Remove duplicates intelligently
    # ---------------------------------------

    best_generic = {}

    for medicine in medicines:

        generic = medicine["generic"].lower().strip()

        if generic not in best_generic:

            best_generic[generic] = medicine

        else:

            if medicine["ai_score"] > best_generic[generic]["ai_score"]:

                best_generic[generic] = medicine

    medicines = list(best_generic.values())

    # ---------------------------------------
    # Sort by AI confidence
    # ---------------------------------------

    medicines.sort(
        key=lambda x: x["ai_score"],
        reverse=True
    )

    return medicines

# ==========================================
# PRESCRIPTION INFORMATION PARSER
# ==========================================

def extract_prescription_information(ocr_text, medicines):

    lines = ocr_text.split("\n")

    results = []

    for medicine in medicines:

        info = {

            "medicine": medicine["medicine"],

            "generic": medicine["generic"],

            "confidence": medicine["confidence"],

            "confidence_level": medicine["confidence_level"],

            "dose": "Not Found",

            "frequency": "Not Found",

            "duration": "Not Found",

            "instruction": "Not Found"

        }

        for line in lines:

            lower = line.lower()

            if medicine["medicine"] in lower:

                # Dose
                import re

                dose = re.search(
                    r"(\d+\s*(tablet|tab|capsule|cap|ml|mg))",
                    lower
                )

                if dose:
                    info["dose"] = dose.group()

                # Duration
                duration = re.search(
                    r"(\d+\s*day[s]?)",
                    lower
                )

                if duration:
                    info["duration"] = duration.group()

                # Food Instruction
                if "after food" in lower:

                    info["instruction"] = "After Food"

                elif "before food" in lower:

                    info["instruction"] = "Before Food"

                # Frequency

                if "once" in lower:

                    info["frequency"] = "Once Daily"

                elif "twice" in lower:

                    info["frequency"] = "Twice Daily"

                elif "thrice" in lower:

                    info["frequency"] = "Three Times Daily"

        results.append(info)

    return results

# ==========================================
# TOKEN WINDOW
# ==========================================
# ==========================================
# NORMALIZE MEDICINE NAME
# ==========================================

import re

def normalize_medicine_name(name):

    name = name.lower()

    # Remove spaces and punctuation
    name = re.sub(r"[^a-z0-9]", "", name)

    return name
# ==========================================
# ADAPTIVE TOKEN WINDOW
# ==========================================

# ==========================================
# ADAPTIVE TOKEN WINDOW
# Production V2.1
# ==========================================

def get_token_window(text, medicine_name, all_medicines):

    words = text.lower().split()

    normalized_medicine = normalize_medicine_name(medicine_name)

    start = -1

    # --------------------------------------
    # Find current medicine
    # --------------------------------------

    for i in range(len(words)):

        current = normalize_medicine_name(words[i])

        if i + 1 < len(words):
            current += normalize_medicine_name(words[i + 1])

        if normalized_medicine in current:

            start = i
            break

    if start == -1:
        return []

    end = len(words)

    # --------------------------------------
    # Window Stop Words
    # --------------------------------------

    stop_words = {

        "advice",
        "follow",
        "review",
        "doctor",
        "registration",
        "signature",
        "diagnosis",
        "consultant",
        "reg.",
        "hospital"

    }

    # --------------------------------------
    # Find end of current medicine block
    # --------------------------------------

    for i in range(start + 1, len(words)):

        current_word = words[i].lower()
        if (
    i > start
    and words[i].endswith(".")
    and words[i][:-1].isdigit()
):
         end = i
         break

        # Stop at General Advice etc.
        if current_word in stop_words:

            end = i
            break

        # Stop at next detected medicine

        for med in all_medicines:

            if med["medicine"] == medicine_name:
                continue

            next_name = normalize_medicine_name(
                med["medicine"]
            )

            current = normalize_medicine_name(words[i])

            if i + 1 < len(words):
                current += normalize_medicine_name(
                    words[i + 1]
                )

            if next_name in current:

                end = i
                break

        if end != len(words):
            break

    return words[start:end]

# ==========================================
# STRENGTH + DOSE EXTRACTOR
# ==========================================

import re

# ==========================================
# STRENGTH + DOSE EXTRACTOR
# Production V2.1
# ==========================================

def extract_strength_and_dose(window):

    text = " ".join(window).lower()

    strength = "Not Found"
    dose = "Not Found"

    # ----------------------------------
    # Strength (mg/ml first)
    # ----------------------------------

    match = re.search(

        r"\b(\d+)\s*(mg|mcg|g|ml)\b",

        text

    )

    if match:

        strength = match.group()

    # ----------------------------------
    # Brand Number
    # Example:
    # PAN 40
    # DOLO 650
    # AZEE 500
    # ----------------------------------

    if strength == "Not Found":

        words = text.split()

        if len(words) >= 2:

            if words[1].isdigit():

                strength = words[1]

    # ----------------------------------
    # Dose
    # ----------------------------------

    dose_match = re.search(

        r"\b([1-5])\s*(tablet|tab|capsule|cap|ml)\b",

        text

    )

    if dose_match:

        dose = dose_match.group()

    # OCR sometimes misses the number

    elif "tablet" in text:

        dose = "1 tablet"

    elif "capsule" in text:

        dose = "1 capsule"

    return {

        "strength": strength,

        "dose": dose

    }


# ==========================================
# FREQUENCY EXTRACTOR
# ==========================================

# ==========================================
# FREQUENCY EXTRACTOR
# ==========================================

import re

def extract_frequency(window):

    text = " ".join(window).lower()

    frequency_patterns = {

        "Once Daily": [
            r"\bonce daily\b",
            r"\bonce\b",
            r"\bod\b",
            r"\b1-0-0\b"
        ],

        "Twice Daily": [
            r"\btwice daily\b",
            r"\btwice\b",
            r"\bbd\b",
            r"\b1-0-1\b"
        ],

        "Three Times Daily": [
            r"\bthree times daily\b",
            r"\bthrice daily\b",
            r"\bthrice\b",
            r"\btds\b",
            r"\b1-1-1\b"
        ],

        "Four Times Daily": [
            r"\bqid\b",
            r"\b4 times daily\b",
            r"\b1-1-1-1\b"
        ]
    }

    for label, patterns in frequency_patterns.items():

        for pattern in patterns:

            if re.search(pattern, text):

                return label

    return "Not Found"

# ==========================================
# DURATION + FOOD INSTRUCTION EXTRACTOR
# ==========================================


import re

def extract_duration_instruction(window):

    text = " ".join(window).lower()

    duration = "Not Found"
    instruction = "Not Found"

    # --------------------------------------
    # OCR Corrections
    # --------------------------------------

    text = text.replace("instruetion", "instruction")
    text = text.replace("instrution", "instruction")
    text = text.replace("alter food", "after food")
    text = text.replace("afier food", "after food")
    text = text.replace("ater food", "after food")
    text = text.replace("befere food", "before food")
    text = text.replace("befor food", "before food")

    
    # --------------------------------------
    # Duration
    # --------------------------------------

    duration_patterns = [

        r"\b\d+\s*day\b",
        r"\b\d+\s*days\b",
        r"\b\d+\s*week\b",
        r"\b\d+\s*weeks\b",
        r"\b\d+\s*month\b",
        r"\b\d+\s*months\b",

        # OCR versions
        r"\b\d+\s*ays\b",
        r"\b\d+\s*days?\b"

    ]

    for pattern in duration_patterns:

        match = re.search(pattern, text)

        if match:

            value = match.group()

            #value = value.replace("ays", "Days")
            value = re.sub(
    r"\b(\d+)\s+ays\b",
    r"\1 Days",
    value,
    flags=re.IGNORECASE
)
            value = value.title()

            duration = value

            break

    # --------------------------------------
    # Food Instructions
    # --------------------------------------

    if re.search(r"after\s*food", text):

        instruction = "After Food"

    elif re.search(r"before\s*food", text):

        instruction = "Before Food"

    elif re.search(r"bedtime", text):

        instruction = "At Bedtime"

    elif re.search(r"\baf\b", text):

        instruction = "After Food"

    elif re.search(r"\bbf\b", text):

        instruction = "Before Food"

    elif re.search(r"\bhs\b", text):

        instruction = "At Bedtime"

    return {

        "duration": duration,
        "instruction": instruction

    }    

# ==========================================
# BUILD COMPLETE PRESCRIPTION
# ==========================================

# ==========================================
# BUILD COMPLETE PRESCRIPTION
# Production V2.1
# ==========================================

def build_prescription_information(ocr_text, medicines):

    prescription = []

    for medicine in medicines:

        # ----------------------------------
        # Token Window
        # ----------------------------------

        window = get_token_window(
            ocr_text,
            medicine["medicine"],
            medicines
        )
        print("\n========== WINDOW ==========")
        print("Medicine:", medicine["medicine"])
        print(window)

        # Skip if medicine not found
        if len(window) == 0:
            continue

        # ----------------------------------
        # Extract Information
        # ----------------------------------

        strength_dose = extract_strength_and_dose(window)

        frequency = extract_frequency(window)

        duration_instruction = extract_duration_instruction(window)

        prescription.append({

            "medicine": medicine.get(
                "medicine",
                "Unknown"
            ),

            "generic": medicine.get(
                "generic",
                ""
            ),

            "source": medicine.get(
                "source",
                ""
            ),

            "confidence": medicine.get(
                "confidence",
                0
            ),

            "confidence_level": medicine.get(
                "confidence_level",
                "Low"
            ),

            "strength": strength_dose.get(
                "strength",
                "Not Found"
            ),

            "dose": strength_dose.get(
                "dose",
                "Not Found"
            ),

            "frequency": frequency,

            "duration": duration_instruction.get(
                "duration",
                "Not Found"
            ),

            "instruction": duration_instruction.get(
                "instruction",
                "Not Found"
            )

        })

    # ----------------------------------
    # Remove Duplicate Medicines
    # ----------------------------------

    unique = {}

    for medicine in prescription:

        key = medicine["medicine"].lower()

        if key not in unique:

            unique[key] = medicine

            continue

        # Keep higher confidence version

        if medicine["confidence"] > unique[key]["confidence"]:

            unique[key] = medicine

    return list(unique.values())


if __name__ == "__main__":

    sample = """

    Dolo 650 Tablet

    1 Tablet

    Twice Daily

    3 Days

    After Food

    PAN 40 Tablet

    1 Tablet

    Once Daily

    5 Days

    Before Food

    """

    medicines = extract_medicines_v2(sample)

    prescription = build_prescription_information(
        sample,
        medicines
    )

    print("\n========== FINAL PRESCRIPTION ==========\n")

    for item in prescription:

        print(item)


'''if __name__ == "__main__":

    sample = """

    Dolo 650 Tablet

    1 Tablet

    Twice Daily

    3 Days

    After Food

    PAN 40 Tablet

    1 Tablet

    Once Daily

    5 Days

    Before Food

    """

    medicines = extract_medicines_v2(sample)

    for medicine in medicines:

        window = get_token_window(
            sample,
            medicine["medicine"],
            medicines
        )

        print("\nMedicine :", medicine["medicine"])

        print("Window   :", window)

        info = extract_strength_and_dose(window)

        print("Strength :", info["strength"])

        print("Dose     :", info["dose"])
        print("Frequency:", extract_frequency(window))
        extra = extract_duration_instruction(window)

        print("Duration :", extra["duration"])

        print("Instruction :", extra["instruction"])'''

'''if __name__ == "__main__":

    sample = """

    Dolo 650 Tablet

    1 Tablet

    Twice Daily

    3 Days

    After Food

    PAN 40 Tablet

    1 Tablet

    Once Daily

    5 Days

    Before Food

    """

    medicines = extract_medicines_v2(sample)

    for medicine in medicines:

        window = get_token_window(
            sample,
            medicine["medicine"],
            medicines
        )

        print("\n")
        print(medicine["medicine"])
        print(window)'''

'''if __name__ == "__main__":

    sample = """

    Dolo 650 Tablet

    1 Tablet

    Twice Daily

    3 Days

    After Food

    """

    window = get_token_window(
        sample,
        "dolo 650"
    )

    print(window)'''

