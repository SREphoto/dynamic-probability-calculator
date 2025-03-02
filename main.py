import streamlit as st
import sys
import traceback

print("Starting Streamlit application...")
sys.stdout.flush()

try:
    print("Setting up page config...")
    sys.stdout.flush()

    st.set_page_config(
        page_title="Dynamic Probability Calculator",
        page_icon="🎲",
        layout="wide"
    )

    print("Page config set successfully...")
    sys.stdout.flush()

    st.title("Dynamic Probability Calculator 🎲")
    st.markdown("""
    Welcome to the Probability Calculator! 
    This is a simplified version while we restore full functionality.
    """)

    # Simple test button
    if st.button('Test Button'):
        st.success('Everything is working!')

    print("UI elements rendered successfully...")
    sys.stdout.flush()

except Exception as e:
    print(f"ERROR: Application failed to start: {str(e)}")
    print("Traceback:")
    traceback.print_exc()
    sys.stdout.flush()
    st.error(f"Application Error: {str(e)}")

if __name__ == "__main__":
    print("Starting main function...")
    sys.stdout.flush()