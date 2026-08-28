

import pandas as pd
import re
import json
from rapidfuzz import process, fuzz
from functools import lru_cache
import time

print("SmartMedAI: Loading knowledge bases...")
start_time = time.time()

TWOSIDES_DF = pd.read_parquet('twosides.parquet')
TWOSIDES_DF['drug_1'] = TWOSIDES_DF['drug_1'].str.lower().astype('category')
TWOSIDES_DF['drug_2'] = TWOSIDES_DF['drug_2'].str.lower().astype('category')
TWOSIDES_DF.set_index(['drug_1', 'drug_2'], inplace=True)
TWOSIDES_DF.sort_index(inplace=True)

INDIAN_BRANDS = pd.read_csv('indian_brands.csv')
INDIAN_BRANDS.rename(columns={'brand_name': 'brand', 'generic_name': 'generic'}, inplace=True)
BRAND_TO_GENERIC = dict(zip(INDIAN_BRANDS['brand'].str.lower(), INDIAN_BRANDS['generic'].str.lower()))
ALL_BRANDS = list(BRAND_TO_GENERIC.keys())
GENERIC_ALIASES = {'acetaminophen': 'paracetamol'}

load_time = round(time.time() - start_time, 2)
print(f"Loaded: {len(TWOSIDES_DF)} TWOSIDES records, {len(INDIAN_BRANDS)} brands in {load_time}s")

TRANSLATIONS = {
    'risk_label': {'en': 'Risk Score', 'kn': 'ಅಪಾಯದ ಅಂಕ', 'hi': 'जोखिम स्कोर'},
    'cases_label': {'en': 'Cases', 'kn': 'ವರದಿಯಾದ ಪ್ರಕರಣಗಳು', 'hi': 'मामले'},
    'showing_top_3': {'en': 'Top 3 severe risks shown', 'kn': 'ಅಗ್ರ 3 ತೀವ್ರ ಅಪಾಯಗಳು', 'hi': 'शीर्ष 3 गंभीर जोखिम'},
    'no_interaction': {'en': 'No known interactions', 'kn': 'ಯಾವುದೇ ಸಂವಹನವಿಲ್ಲ', 'hi': 'कोई ज्ञात अंतर्क्रिया नहीं'}
}

def t(key, lang='en'):
    return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get('en', key))

BRAND_CLEANER = re.compile(r'\d+\s*(mg|ml|mcg|g)|tab|cap|syrup|injection|od|bd|tds|hs|sos')

@lru_cache(maxsize=2000)
def normalize_brand(brand_name):
    brand_clean = BRAND_CLEANER.sub('', brand_name.lower()).strip()
    if not brand_clean: return brand_name.lower()
    match = process.extractOne(brand_clean, ALL_BRANDS, scorer=fuzz.ratio)
    generic = BRAND_TO_GENERIC[match[0]] if match and match[1] > 85 else brand_clean
    return GENERIC_ALIASES.get(generic, generic)

def check_drug_pair_ai(drug1, drug2, lang='en'):
    d1, d2 = normalize_brand(drug1), normalize_brand(drug2)
    if d1 == d2: return None
    try: results = TWOSIDES_DF.loc[(d1, d2)]
    except KeyError:
        try: results = TWOSIDES_DF.loc[(d2, d1)]
        except KeyError: return None
    if isinstance(results, pd.Series): results = results.to_frame().T
    if results.empty: return None
    strong_signals = results[(results['PRR'] > 2) & (results['PRR_error'] < 1)].copy()
    if strong_signals.empty: return None
    strong_signals['severity_score'] = strong_signals['PRR'] * strong_signals['reported_count']
    top_risks = strong_signals.sort_values('severity_score', ascending=False).head(3)
    risks = [{
        'condition_en': row['condition_concept_name'],
        'prr': round(row['PRR'], 2),
        'cases': round(row['reported_count'], 2),
        'severity': 'High' if row['PRR'] > 10 else 'Medium' if row['PRR'] > 5 else 'Low',
        'risk_label': t('risk_label', lang),
        'cases_label': t('cases_label', lang)
    } for _, row in top_risks.iterrows()]
    return {
        'pair_display': f"{drug1} + {drug2}",
        'pair_generic': f"{d1} + {d2}",
        'risks': risks,
        'total_signals_found': len(strong_signals),
        'showing_message': t('showing_top_3', lang)
    }

def check_prescription_interactions_ai(drug_list, lang='en'):
    if not drug_list or len(drug_list) < 2:
        return {
            'interactions': [],
            'total_drugs_checked': len(drug_list),
            'total_pairs_checked': 0,
            'has_critical_alerts': False,
            'message': t('no_interaction', lang),
            'lang': lang
        }
    interactions, checked_pairs = [], set()
    for i in range(len(drug_list)):
        for j in range(i + 1, len(drug_list)):
            pair_key = tuple(sorted([drug_list[i], drug_list[j]]))
            if pair_key in checked_pairs: continue
            checked_pairs.add(pair_key)
            result = check_drug_pair_ai(drug_list[i], drug_list[j], lang)
            if result: interactions.append(result)
    return {
        'interactions': interactions,
        'total_drugs_checked': len(drug_list),
        'total_pairs_checked': len(drug_list) * (len(drug_list)-1) // 2,
        'has_critical_alerts': any(r['severity'] == 'High' for i in interactions for r in i['risks']),
        'lang': lang
    }

def check_existing_vs_new(existing_medicines, new_medicines, lang="en"):
    """
    Compare ONLY existing medicines with newly uploaded medicines.

    Existing medicines are never compared with each other.
    New medicines are never compared with each other.
    """

    interactions = []

    for old_med in existing_medicines:

        for new_med in new_medicines:

            result = check_drug_pair_ai(
                old_med,
                new_med,
                lang
            )

            if result:
                interactions.append(result)

    return {
        "interactions": interactions,
        "existing_count": len(existing_medicines),
        "new_count": len(new_medicines),
        "pairs_checked": len(existing_medicines) * len(new_medicines),
        "has_critical_alerts": any(
            risk["severity"] == "High"
            for interaction in interactions
            for risk in interaction["risks"]
        ),
        "lang": lang
    }


if __name__ == "__main__":
    print("\n--- Testing SmartMedAI Interaction Engine ---")
    test_drugs = ['Dolo 650', 'Ecosprin 75', 'Glycomet 500', 'Atorva 10']
    start = time.time()
    output = check_prescription_interactions_ai(test_drugs, lang='en')
    end = time.time()
    print(f"\nInput: {test_drugs}")
    print(f"Latency: {round((end-start)*1000, 1)}ms")
    print(f"Pairs checked: {output['total_pairs_checked']}")
    print(f"\nOutput:\n{json.dumps(output, indent=2)}")