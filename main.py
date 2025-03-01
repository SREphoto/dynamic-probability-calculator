import streamlit as st
import numpy as np
import pandas as pd
from probability_calculator import calculate_probability
from utils import validate_input, format_probability

def load_css():
    with open(".streamlit/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Dynamic Probability Calculator",
        page_icon="🎲",
        layout="wide"
    )
    
    # Load custom CSS
    try:
        load_css()
    except:
        st.warning("Custom CSS file not found. Using default styling.")

    # Initialize session state for variables and past calculations
    if 'variables' not in st.session_state:
        st.session_state.variables = []
    if 'past_calculations' not in st.session_state:
        st.session_state.past_calculations = []

    # Custom header with styling - positioned below Streamlit's menu
    st.markdown("""
    <div style='background-color:#2E3440; padding:4px; position:fixed; top:48px; left:0; right:0; width:100%; z-index:9998; display:flex; justify-content:space-between; align-items:center;' class="sticky-header">
        <div style='width:50px;'></div>
        <h2 style='color:white; text-align:center; margin:0; font-size:18px;' class="header-title">Dynamic Probability Calculator 🎲</h2>
        <button onclick="showInstructions()" style="background:transparent; border:1px solid white; color:white; padding:2px 8px; border-radius:4px; margin-right:10px; cursor:pointer; font-size:12px;">Instructions</button>
    </div>
    
    <div id="instructionsModal" style="display:none; position:fixed; z-index:10000; top:50px; left:50%; transform:translateX(-50%); width:80%; max-width:600px; background:white; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.2); padding:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <h3 style="margin:0;">How to use this calculator</h3>
            <button onclick="hideInstructions()" style="background:none; border:none; font-size:20px; cursor:pointer;">×</button>
        </div>
        <div>
            Calculate probabilities with multiple variables. Add as many variables as needed!
            <br><br>
            <b>Instructions:</b>
            <ol>
                <li>Add variables using the 'Add Variable' button</li>
                <li>Enter values for each variable</li>
                <li>Select calculation type</li>
                <li>View results</li>
            </ol>
        </div>
    </div>

    <script>
        // JavaScript functions to show/hide instructions modal
        function showInstructions() {
            document.getElementById('instructionsModal').style.display = 'block';
        }
        
        function hideInstructions() {
            document.getElementById('instructionsModal').style.display = 'none';
        }
        
        // Close if clicked outside the modal
        window.onclick = function(event) {
            var modal = document.getElementById('instructionsModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
    """, unsafe_allow_html=True)
    
    # Add extra space to prevent content from being hidden under the header
    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
    
    # Main content container with padding for footer
    main_container = st.container()

    with main_container:
        # We removed the expander since we now have the modal

        # Add variable button
        if st.button('Add Variable ➕'):
            st.session_state.variables.append({
                'name': f'Variable {len(st.session_state.variables) + 1}',
                'value': 0.5
            })

        # Display variables
        variables_data = {}
        for idx, var in enumerate(st.session_state.variables):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                new_name = st.text_input(
                    'Variable Name',
                    value=var['name'],
                    key=f'name_{idx}'
                )
                var['name'] = new_name

            with col2:
                new_value = st.number_input(
                    'Probability (0-1)',
                    min_value=0.0,
                    max_value=1.0,
                    value=float(var['value']),
                    key=f'value_{idx}',
                    format="%.4f"
                )
                var['value'] = new_value
                variables_data[new_name] = new_value

            with col3:
                if st.button('Remove ❌', key=f'remove_{idx}'):
                    st.session_state.variables.pop(idx)
                    st.rerun()

        # Calculation options
        if st.session_state.variables:
            st.subheader("Calculation Options")
            calc_type = st.selectbox(
                "Select Probability Calculation",
                ["Joint Probability (AND)",
                 "Union Probability (OR)",
                 "Conditional Probability"]
            )

            # Conditional probability options
            if calc_type == "Conditional Probability" and len(st.session_state.variables) >= 2:
                event_A = st.selectbox("Select Event A (Given)", 
                                     [var['name'] for var in st.session_state.variables])
                event_B = st.selectbox("Select Event B (Target)", 
                                     [var['name'] for var in st.session_state.variables 
                                      if var['name'] != event_A])

            # Calculate button
            if st.button('Calculate Probability'):
                if validate_input(variables_data):
                    try:
                        if calc_type == "Conditional Probability" and len(st.session_state.variables) >= 2:
                            result = calculate_probability(
                                variables_data,
                                calc_type,
                                event_A=event_A,
                                event_B=event_B
                            )
                        else:
                            result = calculate_probability(variables_data, calc_type)

                        # Store calculation in history
                        calculation_record = {
                            'type': calc_type,
                            'variables': variables_data.copy(),
                            'result': result,
                            'id': len(st.session_state.past_calculations)
                        }
                        st.session_state.past_calculations.append(calculation_record)

                        # Display results
                        st.subheader("Results")
                        st.markdown(f"""
                        **Calculation Type:** {calc_type}  
                        **Result:** {format_probability(result)}
                        """)

                        # Add formula display
                        st.markdown("### Formula Used")
                        if calc_type == "Joint Probability (AND)":
                            st.latex(r"P(A \cap B) = P(A) \times P(B)")
                        elif calc_type == "Union Probability (OR)":
                            st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
                        else:
                            st.latex(r"P(B|A) = \frac{P(A \cap B)}{P(A)}")

                    except Exception as e:
                        st.error(f"Calculation Error: {str(e)}")
                else:
                    st.error("Please ensure all probabilities are between 0 and 1.")
        else:
            st.info("Add variables to start calculating probabilities!")

    # Footer
    footer = st.container()
    with footer:
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("New Calculation 🔄"):
                st.session_state.variables = []
                st.rerun()

        with col2:
            st.subheader("Past Calculations")
            if st.session_state.past_calculations:
                for calc in reversed(st.session_state.past_calculations[-5:]):  # Show last 5 calculations
                    with st.expander(f"{calc['type']} - Result: {format_probability(calc['result'])}"):
                        st.write("Variables used:")
                        for var_name, var_value in calc['variables'].items():
                            st.write(f"- {var_name}: {format_probability(var_value)}")
                        if st.button("Use Result as New Variable", key=f"use_{calc['id']}"):
                            st.session_state.variables.append({
                                'name': f"Previous_{calc['type']}_{calc['id']}",
                                'value': calc['result']
                            })
                            st.rerun()
            else:
                st.info("No past calculations yet.")

if __name__ == "__main__":
    main()