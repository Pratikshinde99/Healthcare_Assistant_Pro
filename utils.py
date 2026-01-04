import re
import difflib
import os
import json
from typing import Optional, Dict
try:
    import requests
except Exception:
    requests = None
from data import MEDICATIONS, SYMPTOMS_DB, WELLNESS_DB, EMERGENCY_KEYWORDS, DISCLAIMER

def normalize(text: str) -> str:
    """Normalize text for consistent searching."""
    return re.sub(r"\s+", " ", text.strip()).lower()

def is_emergency(text: str) -> bool:
    """Check if the text contains emergency keywords."""
    text = normalize(text)
    return any(k in text for k in EMERGENCY_KEYWORDS)

def analyze_wellness(text: str) -> str:
    """Check for general wellness topics."""
    text = normalize(text)
    found_topics = []
    
    for topic, advice in WELLNESS_DB.items():
        if topic in text:
            found_topics.append((topic, advice))
            
    if not found_topics:
        return None
        
    response = ""
    for topic, advice in found_topics:
        response += f"Wellness Topic - {topic.capitalize()}: {advice}\n"
        
    return response

def find_medications(text: str):
    """Find known medications (or close matches/aliases) in the text."""
    text = normalize(text)
    words = text.split()
    found = set()
    
    # 1. Exact matches for keys and aliases
    for name, data in MEDICATIONS.items():
        # Check main name
        if re.search(r'\b' + re.escape(name) + r'\b', text):
            found.add(name)
        
        # Check aliases
        for alias in data.get("aliases", []):
            if re.search(r'\b' + re.escape(alias) + r'\b', text):
                found.add(name) # Map alias back to canonical name

    # 2. Fuzzy matching for typos if no exact match found
    if not found:
        # Collect all valid names + aliases
        all_terms = {}
        for name, data in MEDICATIONS.items():
            all_terms[name] = name
            for alias in data.get("aliases", []):
                all_terms[alias] = name
        
        # Check each word in user input against dictionary
        for word in words:
            if len(word) > 3: # Skip short words
                matches = difflib.get_close_matches(word, all_terms.keys(), n=1, cutoff=0.8)
                if matches:
                    canonical_name = all_terms[matches[0]]
                    found.add(canonical_name)

    return list(found)

def check_interaction(med_a: str, med_b: str) -> str:
    """Check interactions between two medications."""
    med_a = normalize(med_a)
    med_b = normalize(med_b)
    
    # Resolve aliases if needed (simple lookup)
    # This assumes the input comes from the dropdown which is already canonical, 
    # but if manually typed, we might need to resolve.
    # For now, we assume dropdown inputs are canonical keys.
    
    a_data = MEDICATIONS.get(med_a)
    b_data = MEDICATIONS.get(med_b)

    if not a_data or not b_data:
        return (
            f"I don't have full interaction details for '{med_a}' and '{med_b}'. "
            f"Please consult a pharmacist or doctor.\n\n{DISCLAIMER}"
        )

    # Check if med_b is in med_a's interaction list or vice versa
    interaction_found = False
    details = []

    if med_b in a_data.get("interactions", []):
        interaction_found = True
        details.append(f"{med_a.capitalize()} is known to interact with {med_b}.")
    
    if med_a in b_data.get("interactions", []):
        interaction_found = True
        # Avoid duplicate message if already added
        msg = f"{med_b.capitalize()} is known to interact with {med_a}."
        if msg not in details:
            details.append(msg)
            
    # Also check category interactions (generic logic simulation)
    # e.g. two NSAIDs
    if a_data.get("category") == b_data.get("category"):
         interaction_found = True
         details.append(f"Both medications are in the '{a_data['category']}' category. Taking them together may increase side effects.")

    if interaction_found:
        return (
            f"**⚠️ Potential Interaction Detected:**\n\n"
            + "\n".join(details) +
            f"\n\n**Recommendation:** Consult your healthcare provider before combining these.\n\n{DISCLAIMER}"
        )
    else:
        return (
            f"No specific known interaction found between **{med_a.capitalize()}** and **{med_b.capitalize()}** in my database.\n"
            f"However, always confirm with a professional.\n\n{DISCLAIMER}"
        )

def analyze_symptoms(text: str) -> str:
    """Analyze text for symptoms and provide advice."""
    text = normalize(text)
    detected_symptoms = []
    
    for symptom, data in SYMPTOMS_DB.items():
        if symptom in text:
            detected_symptoms.append((symptom, data))
            
    if not detected_symptoms:
        # Try fuzzy match for symptoms too
        for word in text.split():
            matches = difflib.get_close_matches(word, SYMPTOMS_DB.keys(), n=1, cutoff=0.8)
            if matches:
                symptom = matches[0]
                if (symptom, SYMPTOMS_DB[symptom]) not in detected_symptoms:
                    detected_symptoms.append((symptom, SYMPTOMS_DB[symptom]))

    if not detected_symptoms:
        return None
        
    response = ""
    for symptom, data in detected_symptoms:
        response += f"Symptom: {symptom.capitalize()}\n"
        response += f"Possible Causes: {', '.join(data['possible_causes'])}\n"
        response += f"Home Care: {data['recommendations']}\n"
        response += f"Red Flags: {data['red_flags']}\n\n"
        
    return response

def openfda_lookup(name: str) -> Optional[Dict[str, str]]:
    if not requests:
        return None
    try:
        q = name.replace(" ", "+")
        url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{q}+openfda.generic_name:{q}&limit=1"
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return None
        data = r.json()
        results = data.get("results")
        if not results:
            return None
        doc = results[0]
        info = {}
        def get_field(k):
            v = doc.get(k)
            if isinstance(v, list):
                return v[0]
            return v
        info["purpose"] = get_field("purpose") or ""
        info["indications"] = get_field("indications_and_usage") or ""
        info["warnings"] = get_field("warnings") or ""
        info["contraindications"] = get_field("contraindications") or ""
        info["adverse_reactions"] = get_field("adverse_reactions") or ""
        return info
    except Exception:
        return None

def get_medication_details(name: str, profile: dict = None) -> str:
    """Get detailed info for a medication, optionally checking profile warnings."""
    data = MEDICATIONS.get(name)
    if not data:
        return None
    info = (
        f"Medication: {name.capitalize()}\n"
        f"Category: {data.get('category', 'Unknown')}\n"
        f"Uses: {data['uses']}\n"
        f"Warnings: {data['warnings']}\n"
        f"Contraindications: {data.get('contraindications', 'None listed')}\n"
        f"Possible Side Effects: {data['side_effects']}\n"
    )
    fda = openfda_lookup(name)
    if fda:
        if fda.get("purpose"):
            info += f"\nFDA Purpose: {fda['purpose']}\n"
        if fda.get("indications"):
            info += f"FDA Indications: {fda['indications'][:400]}...\n"
        if fda.get("warnings"):
            info += f"FDA Warnings: {fda['warnings'][:400]}...\n"
        if fda.get("contraindications"):
            info += f"FDA Contraindications: {fda['contraindications'][:400]}...\n"
        if fda.get("adverse_reactions"):
            info += f"FDA Adverse Reactions: {fda['adverse_reactions'][:400]}...\n"
    info += "\nA healthcare professional can decide whether this medicine is appropriate for you.\n"
    
    # Profile-based warnings
    if profile:
        warnings = []
        age = profile.get("age")
        conditions = normalize(profile.get("conditions", ""))
        
        if age and age < 12:
            warnings.append(f"This medication may not be suitable for children (Age: {age}).")
        if "liver" in conditions and "liver" in data.get("warnings", "").lower():
             warnings.append("Health Alert: Use caution given your history of liver issues.")
        if "kidney" in conditions and "kidney" in data.get("warnings", "").lower():
             warnings.append("Health Alert: Use caution given your history of kidney issues.")
        if "ulcer" in conditions and "stomach" in data.get("warnings", "").lower():
             warnings.append("Health Alert: This medication can affect the stomach.")
             
        if warnings:
            info += "\nPersonalized Alerts based on your profile:\n"
            for w in warnings:
                info += f"- {w}\n"
                
    return info

def infermedica_triage(user_input: str, profile: dict = None) -> Dict[str, str]:
    text = normalize(user_input)
    app_id = os.getenv("INFERMEDICA_APP_ID")
    app_key = os.getenv("INFERMEDICA_APP_KEY")
    if requests and app_id and app_key:
        try:
            headers = {
                "App-Id": app_id,
                "App-Key": app_key,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            age = (profile or {}).get("age") or 30
            sex = "female"
            payload = {"age": {"value": age}, "sex": sex, "evidence": []}
            url = "https://api.infermedica.com/v3/triage"
            r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=8)
            if r.status_code == 200:
                tr = r.json()
                lvl = tr.get("triage_level") or "unknown"
                return {"level": lvl, "source": "infermedica"}
        except Exception:
            pass
    if is_emergency(text):
        return {"level": "emergency", "source": "heuristic"}
    keywords = ["severe", "high fever", "blood", "bloody", "difficulty breathing", "chest pain", "fainting"]
    if any(k in text for k in keywords):
        return {"level": "doctor_visit", "source": "heuristic"}
    symptoms = []
    for s in SYMPTOMS_DB.keys():
        if s in text:
            symptoms.append(s)
    if symptoms:
        return {"level": "self_care", "source": "heuristic"}
    return {"level": "unknown", "source": "heuristic"}
