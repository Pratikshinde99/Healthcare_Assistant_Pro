import os
from dotenv import load_dotenv

load_dotenv()

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import streamlit as st
import transformers
from data import MEDICATIONS, DISCLAIMER
from utils import (
    is_emergency, 
    find_medications, 
    get_medication_details, 
    check_interaction, 
    analyze_symptoms,
    analyze_wellness,
    normalize,
    infermedica_triage
)

# Page Configuration must be the first streamlit command
st.set_page_config(
    page_title="Healthcare Assistant Pro",
    page_icon="🩺",
    layout="wide"
)

# Initialize global state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'profile' not in st.session_state:
    st.session_state.profile = {"name": "Guest", "age": 30, "conditions": ""}

# Load Model (Cached)
@st.cache_resource
def load_model():
    # Upgrade to 'base' for better reasoning/RAG capabilities
    return transformers.pipeline("text2text-generation", model="google/flan-t5-base")

try:
    text_generator = load_model()
except Exception as e:
    st.error(f"Error loading AI model: {e}")
    text_generator = None

def available_backends():
    # Priority: Groq (Llama-3) > OpenAI > Anthropic > Local
    backends = []
    
    if os.getenv("GROQ_API_KEY"):
        try:
            import groq  # type: ignore
            backends.append("Groq (Llama-3.1-70B)")
        except Exception:
            pass

    if os.getenv("OPENAI_API_KEY"):
        try:
            import openai  # type: ignore
            backends.append("OpenAI (gpt-4o-mini)")
        except Exception:
            pass

    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            import anthropic  # type: ignore
            backends.append("Anthropic (Claude 3.5)")
        except Exception:
            pass
            
    backends.append("Local (FLAN-T5-Base)")
    return backends

MASTER_PROMPT = (
    "You are an AI Health Navigator and Clinical Guidance Assistant.\n"
    "Provide accurate, evidence-based medical information. Explain symptoms, conditions, and treatments in simple language. "
    "Help users understand severity and next steps. Support informed decision-making.\n"
    "Strict rules:\n"
    "1) Do NOT diagnose diseases.\n"
    "2) Do NOT prescribe medications or dosages.\n"
    "3) Do NOT claim to replace a doctor.\n"
    "4) Always recommend professional medical consultation when risk exists.\n"
    "5) Use conditional, safety-aware language.\n"
    "Allowed: symptom explanation; possible causes (non-diagnostic); risk awareness; lifestyle and preventive advice; "
    "medicine purpose, side effects, and warnings (no dosage); informational interpretation of medical reports.\n"
    "Emergency handling: If symptoms suggest emergency, immediately advise seeking emergency medical care and do not continue normal conversation.\n"
    "Tone: calm, professional, reassuring, clear.\n"
    "Output: clear headings, bullet points where helpful, short readable explanations, end with a medical safety note.\n"
)

def generate_via_openai(prompt: str) -> str | None:
    try:
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": MASTER_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return resp.choices[0].message.content
    except Exception:
        return None

def generate_via_anthropic(prompt: str) -> str | None:
    try:
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=600,
            temperature=0.6,
            messages=[{"role": "user", "content": MASTER_PROMPT + "\n\n" + prompt}]
        )
        return "".join([b.text for b in msg.content if hasattr(b, "text")])
    except Exception:
        return None

def generate_via_groq(prompt: str) -> str | None:
    try:
        from groq import Groq
        client = Groq()
        resp = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": MASTER_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return resp.choices[0].message.content
    except Exception:
        return None

def generate_ai_response(user_input: str, context: str = "") -> str:
    if not text_generator:
        return "AI model is currently unavailable."
        
    if context:
        prompt = (
            "Use the following medical context to provide safe guidance and explanations without diagnosing or prescribing. "
            "If the context is insufficient, provide general safety-aware advice. "
            f"Context: {context} "
            f"Patient Question: {user_input} "
            "Answer:"
        )
    else:
        prompt = (
            "Answer the following health question safely, briefly and clearly. "
            "Do not diagnose or prescribe. "
            f"Question: {user_input} "
            "Answer:"
        )
    
    try:
        backend = st.session_state.get("model_backend", "Local (FLAN-T5-Base)")
        if backend == "Local (FLAN-T5-Base)":
            out = text_generator(
                MASTER_PROMPT + "\n\n" + prompt, 
                max_length=256, 
                min_length=20, 
                do_sample=True, 
                temperature=0.6, 
                top_p=0.9,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
            return out[0]["generated_text"]
        if backend == "OpenAI (gpt-4o-mini)":
            r = generate_via_openai(prompt)
            if r:
                return r
        if backend == "Anthropic (Claude 3.5)":
            r = generate_via_anthropic(prompt)
            if r:
                return r
        if backend == "Groq (Llama-3.1-70B)":
            r = generate_via_groq(prompt)
            if r:
                return r
        out = text_generator(
            MASTER_PROMPT + "\n\n" + prompt, 
            max_length=256, 
            min_length=20, 
            do_sample=True, 
            temperature=0.6, 
            top_p=0.9,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3
        )
        return out[0]["generated_text"]
    except Exception:
        return "I am unable to generate a response at this moment."

def process_input(user_input: str):
    triage = infermedica_triage(user_input, st.session_state.profile)
    if triage.get("level") == "emergency" or is_emergency(user_input):
        return (
            "🚨 **CRITICAL WARNING** 🚨\n\n"
            "Your query contains keywords indicating a potential medical emergency. "
            "**Please call emergency services (911 or local equivalent) immediately.**\n"
            "Do not rely on this assistant for life-threatening situations."
        )

    context_parts = []
    symptom_advice = analyze_symptoms(user_input)
    if symptom_advice:
        context_parts.append(symptom_advice)

    wellness_advice = analyze_wellness(user_input)
    if wellness_advice:
        context_parts.append(wellness_advice)

    found_meds = find_medications(user_input)
    if found_meds:
        for med in found_meds:
            details = get_medication_details(med, st.session_state.profile)
            if details:
                context_parts.append(details)
    
    if triage.get("level") in {"self_care", "doctor_visit"}:
        context_parts.append(f"Triage Level: {triage['level']}")
    
    context = "\n".join(context_parts)

    ai_response = generate_ai_response(user_input, context)
    if found_meds and len(found_meds) > 1:
        ai_response += "\n\n💡 **Note:** You mentioned multiple medications. Check the 'Interaction Checker' tab for safety."

    header = ""
    lvl = triage.get("level")
    if lvl == "doctor_visit":
        header = "⚠️ Risk Level: Doctor visit recommended.\n\n"
    elif lvl == "self_care":
        header = "ℹ️ Risk Level: Self-care appropriate with monitoring.\n\n"
    elif lvl == "unknown":
        header = "ℹ️ Risk Level: Unable to determine; consider professional advice if concerned.\n\n"
    return f"{header}{ai_response}\n\n---\n{DISCLAIMER}"

def main():
    # --- Sidebar: User Profile ---
    with st.sidebar:
        st.title("👤 Patient Profile")
        st.info("Personalize your experience for better safety warnings.")
        
        st.session_state.profile["name"] = st.text_input("Name", st.session_state.profile["name"])
        st.session_state.profile["age"] = st.number_input("Age", value=st.session_state.profile["age"], min_value=0, max_value=120)
        st.session_state.profile["conditions"] = st.text_area("Medical Conditions (e.g., high blood pressure, diabetes)", st.session_state.profile["conditions"])
        
        st.markdown("---")
        st.caption(f"Active Profile: {st.session_state.profile['name']} ({st.session_state.profile['age']} yrs)")
        st.markdown("---")
        available = available_backends()
        default_backend = available[0] if available else "Local (FLAN-T5-Base)"
        st.session_state.model_backend = st.selectbox("Model Backend", available, index=available.index(default_backend) if available else 0)

    # --- Main Interface ---
    st.title("🩺 Healthcare Assistant Pro")
    st.markdown(
        """
        Welcome to your advanced medical companion. 
        I can help you understand medications, check interactions, and analyze common symptoms.
        """
    )

    # Tabs for different functionalities
    tab_chat, tab_db, tab_interactions = st.tabs(["💬 Health Chat", "💊 Medication Database", "⚠️ Interaction Checker"])

    # --- Tab 1: Chat Interface ---
    with tab_chat:
        st.subheader("Ask Dr. AI")
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

        # Input area
        if prompt := st.chat_input("Describe your symptoms or ask about a medication..."):
            # User message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Assistant message
            with st.chat_message("assistant"):
                with st.spinner("Analyzing medical database..."):
                    response = process_input(prompt)
                    st.markdown(response)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # --- Tab 2: Medication Database ---
    with tab_db:
        st.subheader("Browse Medication Encyclopedia")
        selected_med = st.selectbox("Select a medication:", sorted(MEDICATIONS.keys()))
        
        if selected_med:
            details = get_medication_details(selected_med, st.session_state.profile)
            st.markdown(details)
            
    # --- Tab 3: Interaction Checker ---
    with tab_interactions:
        st.subheader("Drug-Drug Interaction Checker")
        col1, col2 = st.columns(2)
        with col1:
            med_a = st.selectbox("Medication A", sorted(MEDICATIONS.keys()), key="int_a")
        with col2:
            med_b = st.selectbox("Medication B", sorted(MEDICATIONS.keys()), key="int_b") # simplified for UI
            
        if st.button("Check Interactions"):
            if med_a == med_b:
                st.warning("Please select two different medications.")
            else:
                result = check_interaction(med_a, med_b)
                if "⚠️" in result:
                    st.error(result)
                else:
                    st.success(result)

if __name__ == "__main__":
    main()
