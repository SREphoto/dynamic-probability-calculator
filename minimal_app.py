import streamlit as st
import sys

print("Starting minimal Streamlit app...")
sys.stdout.flush()

st.set_page_config(
    page_title="Minimal Test",
    page_icon="🔍",
    layout="wide"
)

print("Page config set...")
sys.stdout.flush()

st.title("Minimal Streamlit Test")
st.write("Hello World!")
st.info("Server is running on port 5000")

print("UI elements rendered...")
sys.stdout.flush()
