MEDICATIONS = {
    "paracetamol": {
        "aliases": ["tylenol", "acetaminophen", "panadol"],
        "uses": "Pain reliever and fever reducer.",
        "dosage_adult": "500mg-1000mg every 4-6 hours, max 4000mg/day.",
        "dosage_pediatric": "10-15mg/kg every 4-6 hours.",
        "warnings": "Liver damage risk with overdose. Avoid alcohol.",
        "contraindications": "Severe liver disease.",
        "side_effects": "Nausea, rash (rare).",
        "interactions": ["alcohol", "warfarin", "isoniazid"],
        "category": "Analgesic"
    },
    "ibuprofen": {
        "aliases": ["advil", "motrin", "brufen"],
        "uses": "Anti-inflammatory, pain relief, fever reduction.",
        "dosage_adult": "200mg-400mg every 4-6 hours, max 3200mg/day (prescription) or 1200mg/day (OTC).",
        "dosage_pediatric": "5-10mg/kg every 6-8 hours.",
        "warnings": "Stomach bleeding risk, kidney damage risk. Take with food.",
        "contraindications": "Active stomach ulcer, severe heart failure, third trimester pregnancy.",
        "side_effects": "Stomach pain, heartburn, dizziness.",
        "interactions": ["aspirin", "lisinopril", "warfarin", "lithium"],
        "category": "NSAID"
    },
    "aspirin": {
        "aliases": ["acetylsalicylic acid", "disprin", "ecotrin"],
        "uses": "Pain relief, fever reduction, heart attack/stroke prevention (low dose).",
        "dosage_adult": "325mg-650mg every 4 hours for pain; 81mg daily for heart protection.",
        "dosage_pediatric": "Avoid in children/teens (Reye's syndrome risk).",
        "warnings": "Bleeding risk. Stop before surgery.",
        "contraindications": "Bleeding disorders, stomach ulcers, allergy to NSAIDs.",
        "side_effects": "Nausea, vomiting, bleeding.",
        "interactions": ["ibuprofen", "warfarin", "methotrexate"],
        "category": "NSAID/Salicylate"
    },
    "amoxicillin": {
        "aliases": ["amoxil", "moxatag"],
        "uses": "Antibiotic for bacterial infections.",
        "dosage_adult": "250mg-500mg every 8 hours or 500mg-875mg every 12 hours.",
        "dosage_pediatric": "20-40mg/kg/day in divided doses.",
        "warnings": "Finish full course. Watch for allergic reactions.",
        "contraindications": "Penicillin allergy.",
        "side_effects": "Diarrhea, nausea, rash.",
        "interactions": ["allopurinol", "probenecid", "warfarin"],
        "category": "Antibiotic"
    },
    "lisinopril": {
        "aliases": ["prinivil", "zestril"],
        "uses": "High blood pressure, heart failure.",
        "dosage_adult": "10mg-40mg daily.",
        "dosage_pediatric": "Determined by specialist.",
        "warnings": "Dry cough, dizziness upon standing. Monitor kidney function.",
        "contraindications": "History of angioedema, pregnancy.",
        "side_effects": "Cough, dizziness, headache.",
        "interactions": ["ibuprofen", "potassium supplements", "lithium"],
        "category": "ACE Inhibitor"
    },
    "atorvastatin": {
        "aliases": ["lipitor"],
        "uses": "Lowers cholesterol, reduces heart attack risk.",
        "dosage_adult": "10mg-80mg daily.",
        "dosage_pediatric": "Determined by specialist.",
        "warnings": "Muscle pain (rhabdomyolysis risk). Avoid grapefruit.",
        "contraindications": "Active liver disease, pregnancy.",
        "side_effects": "Muscle aches, diarrhea, nausea.",
        "interactions": ["erythromycin", "ketoconazole", "grapefruit juice"],
        "category": "Statin"
    },
    "metformin": {
        "aliases": ["glucophage", "fortamet"],
        "uses": "Type 2 diabetes management.",
        "dosage_adult": "500mg-2000mg daily with meals.",
        "dosage_pediatric": "Determined by specialist.",
        "warnings": "Lactic acidosis risk (rare). Kidney monitoring required.",
        "contraindications": "Severe kidney disease, metabolic acidosis.",
        "side_effects": "Nausea, diarrhea, stomach upset.",
        "interactions": ["alcohol", "iodinated contrast dyes", "cimetidine"],
        "category": "Antidiabetic"
    },
    "omeprazole": {
        "aliases": ["prilosec"],
        "uses": "GERD, acid reflux, ulcers.",
        "dosage_adult": "20mg-40mg daily before breakfast.",
        "dosage_pediatric": "Determined by specialist.",
        "warnings": "Long-term use bone fracture risk.",
        "contraindications": "Hypersensitivity.",
        "side_effects": "Headache, abdominal pain.",
        "interactions": ["clopidogrel", "methotrexate"],
        "category": "Proton Pump Inhibitor"
    },
    "cetirizine": {
        "aliases": ["zyrtec"],
        "uses": "Allergy relief (hay fever, hives).",
        "dosage_adult": "5mg-10mg daily.",
        "dosage_pediatric": "2.5mg-10mg daily depending on age.",
        "warnings": "May cause drowsiness.",
        "contraindications": "Severe kidney impairment.",
        "side_effects": "Drowsiness, dry mouth, fatigue.",
        "interactions": ["alcohol", "sedatives"],
        "category": "Antihistamine"
    },
    "azithromycin": {
        "aliases": ["zithromax", "z-pak"],
        "uses": "Antibiotic for respiratory, skin infections.",
        "dosage_adult": "500mg day 1, then 250mg days 2-5 (Z-Pak).",
        "dosage_pediatric": "10mg/kg day 1, then 5mg/kg days 2-5.",
        "warnings": "QT prolongation risk (heart rhythm).",
        "contraindications": "History of cholestatic jaundice with prior use.",
        "side_effects": "Diarrhea, nausea, abdominal pain.",
        "interactions": ["warfarin", "antacids (magnesium/aluminum)"],
        "category": "Antibiotic"
    }
}

SYMPTOMS_DB = {
    "headache": {
        "possible_causes": ["Tension", "Migraine", "Dehydration", "Sinus infection"],
        "recommendations": "Rest in a dark room, hydrate. Over-the-counter pain relief may help if appropriate; consult a professional if unsure.",
        "red_flags": "Sudden severe pain, stiff neck, confusion (Seek emergency care)."
    },
    "fever": {
        "possible_causes": ["Viral infection", "Bacterial infection", "Inflammation"],
        "recommendations": "Rest and fluids. Temperature-lowering measures may help; seek professional advice for medication suitability.",
        "red_flags": "High fever (>103°F/39.4°C), seizure, rash, difficulty breathing."
    },
    "cough": {
        "possible_causes": ["Common cold", "Flu", "Allergies", "Bronchitis"],
        "recommendations": "Honey (if >1yr), hydration, humidifier. Over-the-counter cough relief may help; confirm suitability.",
        "red_flags": "Coughing up blood, shortness of breath, chest pain."
    },
    "stomach pain": {
        "possible_causes": ["Indigestion", "Gas", "Gastritis", "Food poisoning"],
        "recommendations": "Bland diet (BRAT), hydration. Heartburn relief may help if appropriate; seek guidance if uncertain.",
        "red_flags": "Severe pain, bloody stool, vomiting blood."
    },
    "sore throat": {
        "possible_causes": ["Viral infection", "Strep throat", "Allergies"],
        "recommendations": "Salt water gargle, lozenges, hydration.",
        "red_flags": "Difficulty swallowing, drooling, high fever."
    },
    "nausea": {
        "possible_causes": ["Food poisoning", "Virus", "Motion sickness", "Migraine"],
        "recommendations": "Ginger, peppermint, small frequent sips of clear fluids.",
        "red_flags": "Signs of dehydration, blood in vomit, severe abdominal pain."
    },
    "common cold": {
        "possible_causes": ["Rhinovirus", "Coronavirus", "RSV"],
        "recommendations": "Rest, hydration, zinc supplements, saline nasal drops. Decongestant use should be confirmed with a professional.",
        "red_flags": "Symptoms lasting >10 days, high fever, difficulty breathing."
    },
    "flu": {
        "possible_causes": ["Influenza virus A or B"],
        "recommendations": "Rest, plenty of fluids. Antiviral medication is a clinical decision made by a healthcare professional.",
        "red_flags": "Difficulty breathing, chest pain, severe weakness, confusion."
    },
    "runny nose": {
        "possible_causes": ["Cold", "Allergies", "Sinus infection"],
        "recommendations": "Fluids, humidifier, saline spray. Antihistamine use depends on clinical suitability.",
        "red_flags": "Green/yellow discharge with fever, facial pain."
    },
    "congestion": {
        "possible_causes": ["Cold", "Sinusitis", "Allergies"],
        "recommendations": "Steam inhalation, saline spray, elevation of head. Decongestants may help if appropriate; confirm suitability.",
        "red_flags": "Severe headache, vision changes, high fever."
    }
}

WELLNESS_DB = {
    "diet": "Focus on whole foods: vegetables, fruits, lean proteins, whole grains, and healthy fats. Minimize processed sugars and sodium.",
    "exercise": "Aim for at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity per week, plus strength training twice a week.",
    "sleep": "Adults typically need 7-9 hours of quality sleep. Stick to a schedule, avoid screens before bed, and keep the room cool and dark.",
    "hydration": "Drink enough water so that your urine is pale yellow. General rule: 8 glasses (8oz) per day, adjusted for activity and heat.",
    "stress": "Practice mindfulness, deep breathing, or yoga. Maintain social connections and ensure adequate downtime."
}

EMERGENCY_KEYWORDS = [
    "chest pain", "shortness of breath", "severe bleeding", "unconscious", "stroke symptoms",
    "severe allergic reaction", "trouble breathing", "fainting", "heart attack", "suicide",
    "kill myself", "overdose", "poison", "seizure", "crushing pain"
]

DISCLAIMER = (
    "⚠️ **DISCLAIMER:** This AI assistant provides general health and medication information only. "
    "It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. "
    "Dosages mentioned are standard guidelines and may not apply to you. "
    "Always consult a qualified healthcare professional before making decisions about medications."
)
