import streamlit as st
import sys
import traceback

print("Starting minimal Streamlit app...")
sys.stdout.flush()

try:
    # Basic page config
    print("Setting up page config...")
    sys.stdout.flush()

    st.set_page_config(
        page_title="Minimal Test",
        page_icon="🔍",
        layout="wide"
    )
    print("Page config set successfully...")
    sys.stdout.flush()

    # Basic content
    st.title("Minimal Streamlit Test")
    st.write("Hello World!")

    # Add a simple interactive element
    if st.button('Click me!'):
        st.success('Button clicked!')

    print("UI elements rendered successfully...")
    sys.stdout.flush()

except Exception as e:
    print(f"ERROR in minimal app: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
    sys.stdout.flush()
    st.error(f"Application Error: {str(e)}")