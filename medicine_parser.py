import re

def parse_prescription(ocr_text):
    """
    Parse OCR text into medicine, dose and frequency.
    """

    lines = [line.strip() for line in ocr_text.split("\n") if line.strip()]

    medicines = []

    i = 0

    while i < len(lines):

        medicine = lines[i]

        dose = "Not Specified"
        frequency = "Not Specified"

        if i + 1 < len(lines):
            dose = lines[i + 1]

        if i + 2 < len(lines):
            frequency = lines[i + 2]

        medicines.append({
            "medicine": medicine,
            "dose": dose,
            "frequency": frequency
        })

        i += 3

    return medicines


if __name__ == "__main__":

    sample = """
    Dolo 650
    1 tablet after food
    Twice daily

    Glycomet 500
    1 tablet before breakfast
    Once daily
    """

    result = parse_prescription(sample)

    for item in result:

        print(item)