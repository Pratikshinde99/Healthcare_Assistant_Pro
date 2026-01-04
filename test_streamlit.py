import streamlit as st
from transformers import pipeline

st.write("Imported successfully")
try:
    pipe = pipeline("text2text-generation", model="t5-small")
    st.write("Pipeline created")
except Exception as e:
    st.error(f"Error: {e}")
