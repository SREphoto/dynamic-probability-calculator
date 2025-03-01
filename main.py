import streamlit as st
import numpy as np
import pandas as pd
from probability_calculator import calculate_probability
from utils import validate_input, format_probability

def main():
    st.set_page_config(
        page_title="Dynamic Probability Calculator",
        page_icon="🎲",
        layout="wide"
    )

    st.title("Dynamic Probability Calculator 🎲")
    st.markdown("""
    Calculate probabilities with multiple variables. Add as many variables as needed!

    **Instructions:**
    1. Add variables using the 'Add Variable' button
    2. Enter values for each variable
    3. Select calculation type
    4. View results
    """)

    # Initialize session state for variables if not exists
    if 'variables' not in st.session_state:
        st.session_state.variables = []

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
                st.experimental_rerun()

    # Calculation options
    if st.session_state.variables:
        st.subheader("Calculation Options")

        # Create two columns for the calculation type selection and help icon
        calc_col, help_col = st.columns([4, 1])

        with calc_col:
            calc_type = st.selectbox(
                "Select Probability Calculation",
                ["Joint Probability (AND)",
                 "Union Probability (OR)",
                 "Conditional Probability"]
            )

        with help_col:
            if calc_type == "Joint Probability (AND)":
                st.help("""
                Joint Probability calculates the probability of all events occurring together.

                Formula: P(A ∩ B) = P(A) × P(B)

                Example: If P(Rain) = 0.3 and P(Wind) = 0.4
                P(Rain AND Wind) = 0.3 × 0.4 = 0.12
                """)
            elif calc_type == "Union Probability (OR)":
                st.help("""
                Union Probability calculates the probability of at least one event occurring.

                Formula: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

                Example: If P(Rain) = 0.3 and P(Wind) = 0.4
                P(Rain OR Wind) = 0.3 + 0.4 - (0.3 × 0.4) = 0.58
                """)
            else:
                st.help("""
                Conditional Probability calculates the probability of one event occurring given that another event has occurred.

                Formula: P(B|A) = P(A ∩ B) / P(A)

                Example: If P(Rain) = 0.3 and P(Rain AND Thunder) = 0.12
                P(Thunder|Rain) = 0.12 / 0.3 = 0.4
                """)

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

                    # Display results
                    st.subheader("Results")
                    st.markdown(f"""
                    **Calculation Type:** {calc_type}  
                    **Result:** {format_probability(result)}
                    """)

                    # Display formula used
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

if __name__ == "__main__":
    main()