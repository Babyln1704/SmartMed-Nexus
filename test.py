from check import check_drug_pair_ai

pairs = [
    ("pan 40", "sucral"),
    ("pan 40", "gelusil"),
    ("pan 40", "vitamin c"),
    ("pan 40", "zincovit"),
    ("pan 40", "calcium"),
    ("pan 40", "iron"),
    ("pan 40", "levocetirizine"),
    ("pan 40", "thyronorm 50"),
    ("pan 40", "metformin"),
    ("pan 40", "glycomet 500")
]

for d1, d2 in pairs:

    print("="*60)
    print(d1, "+", d2)

    result = check_drug_pair_ai(d1, d2)

    if result:
        print("✅ Interaction")
        print(result["pair_display"])

    else:
        print("❌ No Interaction")