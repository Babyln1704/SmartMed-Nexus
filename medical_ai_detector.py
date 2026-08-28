import re

MEDICINE_KEYWORDS = {

    "tablet",
    "tab",
    "capsule",
    "cap",
    "syrup",
    "cream",
    "ointment",
    "drops",
    "injection",
    "mg",
    "mcg",
    "ml"

}


def split_prescription_lines(text):
    """
    Split OCR into meaningful prescription lines.
    """

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:

            lines.append(line)

    return lines

# ==========================================
# REMOVE HEADER (Production V2)
# ==========================================

import re

def remove_header(lines):
    """
    Removes hospital/doctor/patient header.
    Starts when a probable medicine section begins.
    Works with or without Rx.
    """

    START_WORDS = {
        "rx",
        "prescription",
        "medicine",
        "medicines"
    }

    started = False
    filtered = []

    for line in lines:

        original = line.strip()

        lower = original.lower()

        # -------------------------
        # Explicit headings
        # -------------------------

        if lower in START_WORDS:
            started = True
            continue

        # -------------------------
        # Remove bullets / numbering
        # -------------------------

        temp = re.sub(r'^[\d\.\)\-\•\*]+\s*', '', original)

        words = temp.split()

        # -------------------------
        # Detect medicine-like line
        # -------------------------

        if not started:

            if len(words) >= 2:

                first = words[0]

                second = words[1]

                # Dolo 650
                if first.isalpha() and second.isdigit():

                    started = True

                # Tab Dolo
                elif first.lower() in {"tab","tablet","cap","capsule"}:

                    started = True

                # Cetirizine 10
                elif first[0].isalpha() and any(c.isdigit() for c in second):

                    started = True

        if started:

            filtered.append(temp)

    return filtered
# ==========================================
# REMOVE FOOTER
# ==========================================

def remove_footer(lines):
    """
    Remove only the footer section.
    Do NOT stop on header information.
    """

    footer_keywords = {

        "general advice",
        "advice:",
        "follow up",
        "follow-up",
        "signature",
        "doctor signature",
        "thank you"

    }

    filtered = []

    for line in lines:

        lower = line.lower().strip()

        # Stop only when footer actually starts
        if any(keyword in lower for keyword in footer_keywords):
            break

        filtered.append(line)

    return filtered

# ==========================================
# TABLE FORMAT DETECTOR
# ==========================================

import re

def normalize_table_lines(lines):
    """
    Converts table-style prescriptions into
    normal medicine lines.
    """

    normalized = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # Ignore table headers

        if any(

            word in lower

            for word in [

                "medicine",
                "dose",
                "frequency",
                "duration"

            ]

        ):

            continue

        # Replace table separators

        line = line.replace("|", " ")

        line = re.sub(r"\s+", " ", line)

        normalized.append(line)

    return normalized

import re

def find_medicine_lines(lines):
    """
    Detect probable medicine lines from OCR.
    """

    print("\n========== INPUT TO find_medicine_lines ==========")

    for l in lines:
        print(repr(l))

    medicine_lines = []

    IGNORE_WORDS = {
        "once", "twice", "daily",
        "before", "after", "food",
        "morning", "night",
        "days", "day", "week", "weeks",
        "continue", "review", "follow",
        "advice", "complaint"
    }

    HEADER_WORDS = {
        "phone",
        "patient",
        "patent",
        "name",
        "age",
        "gender",
        "address",
        "diagnosis",
        "doctor",
        "clinic",
        "hospital",
        "date",
        "bangalore",
        "baers"
    }

    BAD_FIRST_WORDS = {
        "does",
        "dose",
        "dore",
        "instruction",
        "instructions",
        "frequency",
        "duration",
        "uration",
        "buraven",
        "general",
        "goneral",
        "follow",
        "review",
        "advice"
    }

    MEDICINE_FORMS = {
        "tablet",
        "tab",
        "capsule",
        "cap",
        "syrup",
        "drops",
        "cream",
        "ointment",
        "injection",
        "inj"
    }

    for line in lines:

        line = (
            line.replace("‘", "")
                .replace("’", "")
                .replace("'", "")
                .replace("`", "")
                .strip()
        )

        if not line:
            continue

        line = re.sub(
            r'^[^A-Za-z]*',
            '',
            line
        )

        words = line.split()

        if not words:
            continue

        first = words[0].lower().rstrip(":")

        # -----------------------------
        # Reject headers
        # -----------------------------

        if first in HEADER_WORDS:
            continue

        # -----------------------------
        # Reject obvious non-medicine
        # -----------------------------

        if first in BAD_FIRST_WORDS:
            continue

        # -----------------------------
        # Reject advice sentences
        # -----------------------------

        lower_words = [w.lower() for w in words]

        if any(word in IGNORE_WORDS for word in lower_words):
            continue

        # -----------------------------
        # Medicine detection
        # -----------------------------

        has_number = any(ch.isdigit() for ch in line)

        ends_with_form = (
            words[-1].lower() in MEDICINE_FORMS
        )

        single_word_medicine = (
            len(words) == 1
            and words[0][0].isalpha()
        )

        if not (
            has_number
            or ends_with_form
            or single_word_medicine
        ):
            continue

        if first[0].isalpha():

            medicine_lines.append(line)

    print("\n========== MEDICINE LINES ==========")
    print(medicine_lines)

    return medicine_lines

def extract_ai_candidates(lines):
    """
    Extract only medicine names from medicine lines.
    """

    candidates = []

    DOSAGE_WORDS = {

        "tablet",
        "tab",
        "capsule",
        "cap",
        "syrup",
        "cream",
        "ointment",
        "drops",
        "injection",
        "before",
        "after",
        "food",
        "daily",
        "once",
        "twice",
        "morning",
        "night"

    }

    for line in lines:

        words = line.split()

        medicine = []

        for word in words:

            clean = re.sub(r"[^A-Za-z0-9]", "", word)

            if not clean:
                continue

            lower = clean.lower()

            if not medicine:

    # Ignore numbering
               if clean.isdigit():
                  continue

    # Ignore short OCR garbage
               if len(clean) <= 2:
                  continue

            # Stop once dosage words start

            if lower in DOSAGE_WORDS:
                break

            medicine.append(clean)

        # -----------------------------
        # Remove trailing dosage words
        # -----------------------------

        while medicine:

            last = medicine[-1].lower()

            if last in DOSAGE_WORDS:

                medicine.pop()

            else:
                break

        if not medicine:
            continue

        # -----------------------------
        # Build medicine name
        # -----------------------------

        # Dolo

        if len(medicine) >= 1:

            candidates.append(

                medicine[0].lower()

            )

        # ----------------------------------
        # Two-word medicines
        # ----------------------------------

        if len(medicine) >= 2:

    # Brand + Strength
            if medicine[1].isdigit():

              candidates.append(

                 medicine[0].lower()
                 + " "
                 + medicine[1]

            )

    # Generic two-word medicines
            else:

                  candidates.append(

                medicine[0].lower()
            + " "
            + medicine[1].lower()

        )
        # Cetirizine 10 mg

        if len(medicine) >= 3:

            if (

                medicine[1].isdigit()

                and

                medicine[2].lower()

                in

                {

                    "mg",
                    "mcg",
                    "ml"

                }

            ):

                candidates.append(

                    medicine[0].lower()
                    + " "
                    + medicine[1]

                )

    return sorted(list(set(candidates)))

# ==========================================
# VERIFY AI CANDIDATES
# ==========================================

def verify_candidates(candidates):
    """
    Remove obviously invalid medicine candidates
    before passing them to match_medicine().
    """

    verified = []

    reject_words = {

        "tablet",
        "tab",
        "capsule",
        "cap",
        "food",
        "before",
        "after",
        "daily",
        "once",
        "twice",
        "morning",
        "night",
        "days",
        "week",
        "weeks",
        "water",
        "doctor",
        "patient",
        "hospital",
        "advice",
        "review",
        "follow",
        "signature"

    }

    for medicine in candidates:

        medicine = medicine.strip().lower()

        if not medicine:
            continue

        words = medicine.split()

        # Reject pure stop words
        if all(word in reject_words for word in words):
            continue

        # Reject single numbers
        if medicine.isdigit():
            continue

        # Reject 1 tablet / 2 tablet etc.
        if len(words) >= 2:

            if words[0].isdigit():

                continue

        verified.append(medicine)

    return sorted(list(set(verified)))

# ==========================================
# REMOVE WEAKER CANDIDATES
# ==========================================

def remove_weaker_candidates(candidates):
    """
    Keep the most informative medicine candidate.

    Example:
    dolo -> removed
    dolo 650 -> kept
    """

    final = []

    candidates = sorted(
        list(set(candidates)),
        key=len,
        reverse=True
    )

    for candidate in candidates:

        keep = True

        for existing in final:

            # existing = longer candidate

            if existing.startswith(candidate + " "):

                keep = False
                break

        if keep:

            final.append(candidate)

    return sorted(final)

def detect_candidates_ai(ocr_text):
    """
    Complete AI Candidate Detection
    """

    lines = split_prescription_lines(
        ocr_text
    )
    print("\n========== SPLIT LINES ==========")
    print(lines)
    lines = remove_header(lines)
    print("\n========== AFTER HEADER ==========")
    print(lines)

    lines = remove_footer(lines)
    print("\n========== AFTER FOOTER ==========")
    print(lines)

    lines = normalize_table_lines(lines)
    print("\n========== AFTER TABLE ==========")
    print(lines)

    medicine_lines = find_medicine_lines(
        lines
    )

    print("\n========== MEDICINE LINES ==========")
    print(medicine_lines)


    candidates = extract_ai_candidates(
        medicine_lines
    )
    print("\n========== AI CANDIDATES ==========")
    print(candidates)
    candidates = verify_candidates(
    candidates
)
    candidates = remove_weaker_candidates(
    candidates
)

    return candidates

if __name__ == "__main__":

    sample = """

    Dolo 650 Tablet

    1 Tablet

    Twice Daily

    PAN 40 Tablet

    1 Tablet

    Once Daily

    Cetirizine 10 mg Tablet

    1 Tablet

    """

    print(detect_candidates_ai(sample))