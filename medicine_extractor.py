import pandas as pd
from rapidfuzz import process, fuzz

print("Loading Medicine Extractor...")

# -----------------------------
# Load Indian Brand Database
# -----------------------------
INDIAN_BRANDS = pd.read_csv("indian_brands.csv")

# Standardize column names
INDIAN_BRANDS.rename(columns={
    "brand_name": "brand",
    "generic_name": "generic"
}, inplace=True)

# Convert everything to lowercase
INDIAN_BRANDS["brand"] = INDIAN_BRANDS["brand"].str.lower()
INDIAN_BRANDS["generic"] = INDIAN_BRANDS["generic"].str.lower()

# Dictionary for brand -> generic conversion
BRAND_TO_GENERIC = dict(
    zip(
        INDIAN_BRANDS["brand"],
        INDIAN_BRANDS["generic"]
    )
)

# List of all medicine brands
ALL_BRANDS = list(BRAND_TO_GENERIC.keys())

print(f"Loaded {len(ALL_BRANDS)} Indian medicine brands.")

# -----------------------------
# Load TWOSIDES Dataset
# -----------------------------
TWOSIDES = pd.read_parquet("twosides.parquet")

TWOSIDES["drug_1"] = TWOSIDES["drug_1"].str.lower()
TWOSIDES["drug_2"] = TWOSIDES["drug_2"].str.lower()

print(f"Loaded {len(TWOSIDES)} TWOSIDES interaction records.")

# ============================================
# FAST LOOKUP TABLES
# ============================================

print("Building lookup tables...")

# All Indian brand names
INDIAN_BRAND_SET = set(ALL_BRANDS)

# All generic medicine names from Indian brands
INDIAN_GENERIC_SET = set(BRAND_TO_GENERIC.values())

# Unique drug names from TWOSIDES
TWOSIDES_DRUGS = set(TWOSIDES["drug_1"]).union(
    set(TWOSIDES["drug_2"])
)

print(f"Indian Brand Set      : {len(INDIAN_BRAND_SET)}")
print(f"Indian Generic Set    : {len(INDIAN_GENERIC_SET)}")
print(f"TWOSIDES Drug Set     : {len(TWOSIDES_DRUGS)}")

import re

# ============================================
# WORDS TO IGNORE
# ============================================

STOP_WORDS = {
    "tab", "tablet", "cap", "capsule",
    "take", "after", "before", "food",
    "morning", "night", "daily", "twice",
    "once", "od", "bd", "tds", "sos", "hs",
    "dr", "doctor", "hospital", "clinic",
    "patient", "name", "age", "sex",
    "review", "continue", "continue.",
    "mg", "ml"
}


# Lists for RapidFuzz search
INDIAN_BRAND_LIST = sorted(INDIAN_BRAND_SET)
TWOSIDES_DRUG_LIST = sorted(TWOSIDES_DRUGS)


import re

def clean_line(line):
    """
    Clean one OCR line before medicine matching.
    """

    # Lowercase
    line = line.lower()

    # Replace separators with spaces
    line = re.sub(r"[-_/]", " ", line)

    # Insert space between letters and numbers
    # dolo650 -> dolo 650
    line = re.sub(r"([a-z]+)(\d{2,})", r"\1 \2", line)

    # Insert space between numbers and letters
    # 650mg -> 650 mg
    line = re.sub(r"(\d{2,})([a-z]+)", r"\1 \2", line)

    # Remove punctuation
    line = re.sub(r"[^\w\s]", " ", line)

    # Remove multiple spaces
    line = " ".join(line.split())

    # Remove stop words
    words = []

    for word in line.split():

        if word not in STOP_WORDS:
            words.append(word)

    return " ".join(words)

# ============================================
# EXACT MEDICINE MATCHING
# ============================================

def exact_match(cleaned_line):
    """
    Checks whether a cleaned OCR line exists
    in Indian Brands or TWOSIDES.
    """

    # Empty line
    if not cleaned_line:
        return None

    # Search Indian Brand names
    if cleaned_line in INDIAN_BRAND_SET:

        return {
            "medicine": cleaned_line,
            "source": "Indian Brand",
            "confidence": 100
        }

    # Search Generic Drug names
    if cleaned_line in TWOSIDES_DRUGS:

        return {
            "medicine": cleaned_line,
            "source": "TWOSIDES",
            "confidence": 100
        }

    return None

# ============================================
# RAPIDFUZZ FALLBACK
# ============================================



def fuzzy_match(cleaned_line):
    """
    If exact match fails, try RapidFuzz.
    """

    if not cleaned_line:
        return None
    

    # -----------------------------
    # Search Indian Brands first
    # -----------------------------
    match = process.extractOne(
        cleaned_line,
        INDIAN_BRAND_LIST,
        scorer=fuzz.WRatio
    )

    if match:

        medicine, score, _ = match

        if score >= 90:

            return {
                "medicine": medicine,
                "source": "Indian Brand (RapidFuzz)",
                "confidence": round(score, 2)
            }

    # -----------------------------
    # Search TWOSIDES drugs
    # -----------------------------
    match = process.extractOne(
        cleaned_line,
        TWOSIDES_DRUG_LIST,
        scorer=fuzz.WRatio
    )

    if match:

        medicine, score, _ = match

        if score >= 90:

            return {
                "medicine": medicine,
                "source": "TWOSIDES (RapidFuzz)",
                "confidence": round(score, 2)
            }

    return None



# ============================================
# MAIN MEDICINE EXTRACTION
# ============================================

def extract_medicines(ocr_text):

    medicines = []

    lines = ocr_text.split("\n")

    for line in lines:

        cleaned = clean_line(line)

        if not cleaned:
            continue

        result = exact_match(cleaned)

        if result is None:
            result = fuzzy_match(cleaned)

        if result:

            medicines.append(result["medicine"])

    # Remove duplicates while preserving order
    medicines = list(dict.fromkeys(medicines))

    return medicines


if __name__ == "__main__":

    sample_text = """

    Apollo Hospital

    Dr Ravi Kumar

    Tab Dolo650

    1 tablet after food

    Glycomet500

    Morning

    Ecosprln75

    Night

    """

    medicines = extract_medicines(sample_text)

    print("\nDetected Medicines\n")

    for medicine in medicines:

        print("✔", medicine)