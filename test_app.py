import streamlit as st
import sys

print("Starting test app initialization...")
sys.stdout.flush()

def main():
    print("Entering main function...")
    sys.stdout.flush()

    print("Setting up Streamlit configuration...")
    sys.stdout.flush()

    st.set_page_config(
        page_title="Test App",
        page_icon="🧪",
        layout="wide"
    )

    print("Streamlit configuration completed")
    sys.stdout.flush()

    st.write("Hello World")
    st.info("Server is ready on port 5000")

    print("Main function completed")
    sys.stdout.flush()

if __name__ == "__main__":
    print("Starting main execution...")
    sys.stdout.flush()
    main()
    print("Main execution completed")
    sys.stdout.flush()