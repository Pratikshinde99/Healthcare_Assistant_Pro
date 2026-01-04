# Healthcare Assistant Pro 🩺

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![AI Powered](https://img.shields.io/badge/AI-LLaMA%20%7C%20GPT--4-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A professional-grade, AI-powered healthcare guidance system designed to perform **symptom triage**, **medical information retrieval**, **risk awareness**, and **personalized health guidance**. 

Unlike generic chatbots, this system follows a strict safety architecture to ensure evidence-based responses without crossing the ethical line into diagnosis or prescription.

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Safety & Ethics](#-safety--ethics)
- [Contact](#-contact)

---

## 🎯 About the Project

In an era of misinformation, looking up symptoms online can be dangerous. **Healthcare Assistant Pro** aims to bridge the gap between "Dr. Google" and a professional medical consultation. 

### Core Objectives
1.  **Primary Aim**: Provide accurate, evidence-based health guidance and symptom severity assessment while safely routing users to professional care when required.
2.  **Secondary Aims**:
    *   Reduce medical misinformation.
    *   Improve early risk awareness (e.g., recognizing stroke signs).
    *   Support doctors by educating patients, not replacing them.
    *   Ensure a deployable, ethical, and safety-first AI solution.

---

## 🚀 Key Features

### 1. Intelligent Symptom Triage
*   **Clinical-Grade Analysis**: Capable of integrating with **Infermedica API** to assess symptom probability and severity.
*   **Emergency Protocols**: Instantly detects life-threatening keywords (e.g., "chest pain", "crushing pressure") and aborts the chat to advise calling emergency services.
*   **Risk Routing**: Classifies cases into *Self-care*, *Doctor Visit*, or *Emergency*.

### 2. Medication Intelligence (OpenFDA)
*   **Official Data Sources**: Pulls real-time drug labels from the **OpenFDA API**.
*   **Safety Checks**: Displays warnings, contraindications, and side effects.
*   **Anti-Misuse**: Deliberately hides dosage information to prevent self-medication errors.
*   **Interaction Checker**: Analyzes potential conflicts between multiple medications.

### 3. Personalized AI Guidance
*   **Profile Context**: Adapts warnings based on user age and existing conditions (e.g., warning a patient with liver issues about specific drugs).
*   **Multi-Model Backend**:
    *   **Groq (LLaMA-3-70B)**: Fast, high-reasoning capability.
    *   **OpenAI (GPT-4o)**: Robust general medical knowledge.
    *   **Local (FLAN-T5)**: Privacy-focused offline fallback.

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | Interactive web UI for chat and data visualization. |
| **Backend Logic** | **Python 3.10+** | Core application logic and API orchestration. |
| **AI / LLM** | **Groq (LLaMA-3)** | Primary reasoning engine (via API). |
| | **OpenAI / Anthropic** | Secondary cloud-based reasoning engines. |
| | **HuggingFace** | Local model support (FLAN-T5). |
| **Data Sources** | **OpenFDA API** | Medication labeling and adverse event data. |
| | **Infermedica API** | Symptom checking and triage (optional). |
| **Environment** | **Dotenv** | Secure API key management. |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10 or higher installed.
- Git installed.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/healthcare-assistant-pro.git
cd healthcare-assistant-pro
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
Create a `.env` file in the root directory to enable AI capabilities.
```env
# AI Providers (Choose at least one)
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk-...

# Optional: Clinical Triage (Free tier available at developer.infermedica.com)
INFERMEDICA_APP_ID=...
INFERMEDICA_APP_KEY=...
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

---

## 🛡 Safety & Ethics

This system adheres to strict **Non-Diagnostic** principles:
1.  **No Diagnosis**: The AI never says "You have X disease." It suggests "Symptoms are consistent with X, Y, Z."
2.  **No Prescriptions**: Specific dosage instructions are blocked.
3.  **Data Privacy**: User profiles are stored in session state only and are not persisted to external databases in this version.
4.  **Continuous Disclaimers**: Every interaction ends with a reminder to consult a professional.

---

## 📬 Contact

For inquiries, collaboration, or support, please contact the lead developer:

**📧 Email**: [ps175581@gmail.com](mailto:ps175581@gmail.com)  

---
*Built with ❤️ for better healthcare accessibility.*
