import streamlit as st
import numpy as np
import pandas as pd
from probability_calculator import calculate_probability
from utils import validate_input, format_probability

def load_css():
    try:
        with open(".streamlit/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")
    except Exception as e:
        st.error(f"An error occurred while loading CSS: {e}")


def main():
    st.set_page_config(
        page_title="Dynamic Probability Calculator",
        page_icon="🎲",
        layout="wide"
    )

    # Check for shared results in URL parameters
    query_params = st.query_params
    shared_result = None

    if "calc_type" in query_params and "result" in query_params and "variables" in query_params:
        shared_result = {
            "calc_type": query_params["calc_type"][0],
            "result": float(query_params["result"][0]),
            "variables": {}
        }

        # Parse variables from URL
        var_str = query_params["variables"][0]
        var_pairs = var_str.split(",")
        for pair in var_pairs:
            if ":" in pair:
                name, value = pair.split(":")
                shared_result["variables"][name] = float(value)

    # Load custom CSS
    load_css()

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
        <div style='width:50px;'></div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for instructions toggle
    if 'show_instructions' not in st.session_state:
        st.session_state.show_instructions = False

    # Add a proper Streamlit button for instructions in the sidebar
    with st.sidebar:
        if st.button('📖 Instructions'):
            st.session_state.show_instructions = not st.session_state.show_instructions

    # Display instructions when toggled
    if st.session_state.show_instructions:
        with st.sidebar:
            st.markdown("### How to use this calculator")
            st.markdown("""
            Calculate probabilities with multiple variables. Add as many variables as needed!

            **Instructions:**
            1. Add variables using the 'Add Variable' button. Each variable represents an event and its probability (0-1).
            2. Enter a descriptive name and the probability for each variable.
            3. Select the desired calculation type from the dropdown menu.
            4. Depending on the calculation type, you might need to select specific variables for different roles (e.g., Event A, Event B) or enter additional parameters.
            5. Click 'Calculate Probability' to see the result and the formula used.

            **Calculation Types:**
            - **Joint Probability (AND):** Calculates the probability of all selected events occurring.
            - **Union Probability (OR):** Calculates the probability of at least one of the selected events occurring.
            - **Conditional Probability:** Calculates P(B|A), the probability of event B occurring given that event A has occurred. Requires selecting two variables.
            - **Bayes' Theorem:** Updates the probability of an event based on new evidence.
              - Select 'Bayes' Theorem' as the calculation type.
              - Choose three of your defined variables for:
                - P(A): The prior probability of event A.
                - P(B|A): The probability of observing evidence B if event A is true.
                - P(B|¬A): The probability of observing evidence B if event A is false.
            - **Binomial Distribution:** Calculates the probability of a specific number of successes in a fixed number of independent trials.
              - Select 'Binomial Distribution' as the calculation type.
              - Choose one of your defined variables for 'p' (probability of success per trial).
              - Enter 'n' (total number of trials) and 'k' (number of successes).
            
            4. View results, including the formula used.
            """)

    # Display past calculations in sidebar
    with st.sidebar:
        st.markdown("---")
        st.subheader("Past Calculations")
        if st.session_state.past_calculations:
            for calc in reversed(st.session_state.past_calculations[-5:]):  # Show last 5 calculations
                with st.expander(f"{calc['type']} - Result: {format_probability(calc['result'])}"):
                    st.write("Variables used:")
                    for var_name, var_value in calc['variables'].items():
                        st.write(f"- {var_name}: {format_probability(var_value)}")
                    if st.button("Use Result as New Variable", key=f"use_sidebar_{calc['id']}"):
                        st.session_state.variables.append({
                            'name': f"Previous_{calc['type']}_{calc['id']}",
                            'value': calc['result']
                        })
                        st.rerun()
        else:
            st.info("No past calculations yet.")

    # Add extra space to prevent content from being hidden under the header
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

    # Main content container with padding for footer
    main_container = st.container()

    with main_container:
        # Display shared results if present
        if shared_result:
            st.info("Viewing shared calculation results")
            st.subheader("Shared Results")
            st.markdown(f"""
            **Calculation Type:** {shared_result['calc_type']}  
            **Result:** {format_probability(shared_result['result'])}

            **Variables used:**
            """)
            for var_name, var_value in shared_result['variables'].items():
                st.markdown(f"- {var_name}: {format_probability(var_value)}")

            if st.button("Start New Calculation"):
                # Clear query parameters by reloading the page
                for param in st.query_params.keys():
                    st.query_params.pop(param)
                st.rerun()

            # Show a horizontal divider
            st.markdown("---")


        # Add variable button
        if st.button('Add Variable ➕'):
            st.session_state.variables.append({
                'name': f'Variable {len(st.session_state.variables) + 1}',
                'value': 0.5
            })

        # Display variables
        variables_data = {}
        for idx, var in enumerate(st.session_state.variables):
            # Create three columns: name, value, and buttons
            name_col, value_col, buttons_col = st.columns([3, 2, 2])

            with name_col:
                new_name = st.text_input(
                    'Variable Name',
                    value=var['name'],
                    key=f'name_{idx}'
                )
                var['name'] = new_name

            with value_col:
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

            with buttons_col:
                # Create two equal columns for the buttons
                remove_btn, add_btn = st.columns(2)
                with remove_btn:
                    if st.button('❌', key=f'remove_{idx}', help="Remove this variable"):
                        st.session_state.variables.pop(idx)
                        st.rerun()
                with add_btn:
                    if st.button('➕', key=f'add_after_{idx}', help="Add new variable"):
                        st.session_state.variables.append({
                            'name': f'Variable {len(st.session_state.variables) + 1}',
                            'value': 0.5
                        })
                        st.rerun()

        # Calculation options
        if st.session_state.variables:
            st.subheader("Calculation Options")
            calc_type = st.selectbox(
                "Select Probability Calculation",
                ["Joint Probability (AND)",
                 "Union Probability (OR)",
                 "Conditional Probability",
                 "Bayes' Theorem",
                 "Binomial Distribution"]
            )

            # Conditional probability options
            event_A = None
            event_B = None
            prior_event_name = None
            evidence_given_prior_event_name = None
            evidence_given_not_prior_event_name = None
            # Binomial distribution options
            prob_success_event_name_binomial = None
            num_trials_binomial = 0
            num_successes_binomial = 0


            if calc_type == "Conditional Probability" and len(st.session_state.variables) >= 2:
                event_A = st.selectbox("Select Event A (Given)",
                                        [var['name'] for var in st.session_state.variables])
                event_B = st.selectbox("Select Event B (Target)",
                                        [var['name'] for var in st.session_state.variables
                                         if var['name'] != event_A])
            elif calc_type == "Bayes' Theorem" and len(st.session_state.variables) >= 3:
                variable_names = [var['name'] for var in st.session_state.variables]
                prior_event_name = st.selectbox("Select P(A) (Prior Probability)", variable_names)
                
                remaining_vars_for_b_given_a = [name for name in variable_names if name != prior_event_name]
                evidence_given_prior_event_name = st.selectbox("Select P(B|A) (Likelihood of evidence if A is true)", remaining_vars_for_b_given_a)
                
                remaining_vars_for_b_given_not_a = [name for name in remaining_vars_for_b_given_a if name != evidence_given_prior_event_name]
                evidence_given_not_prior_event_name = st.selectbox("Select P(B|¬A) (Likelihood of evidence if A is false)", remaining_vars_for_b_given_not_a)
            elif calc_type == "Binomial Distribution":
                prob_success_event_name_binomial = st.selectbox(
                    "Select Variable for Probability of Success (p)",
                    [var['name'] for var in st.session_state.variables]
                )
                num_trials_binomial = st.number_input("Number of Trials (n)", min_value=0, step=1, value=0)
                num_successes_binomial = st.number_input("Number of Successes (k)", min_value=0, step=1, value=0)


            # Calculate button
            if st.button('Calculate Probability'):
                if validate_input(variables_data):
                    try:
                        if calc_type == "Conditional Probability" and len(st.session_state.variables) >= 2:
                            if event_A is None or event_B is None:
                                st.error("Please select both events for conditional probability calculation.")
                                return
                            result = calculate_probability(
                                variables_data,
                                calc_type,
                                event_A=event_A,
                                event_B=event_B
                            )
                        elif calc_type == "Bayes' Theorem" and len(st.session_state.variables) >= 3:
                            if not (prior_event_name and evidence_given_prior_event_name and evidence_given_not_prior_event_name):
                                st.error("Please select all three events for Bayes' Theorem calculation.")
                                return
                            if len(set([prior_event_name, evidence_given_prior_event_name, evidence_given_not_prior_event_name])) < 3:
                                st.error("Please select three distinct variables for Bayes' Theorem calculation.")
                                return
                            result = calculate_probability(
                                variables_data,
                                calc_type,
                                event_A=prior_event_name, # P(A)
                                event_B=evidence_given_prior_event_name, # P(B|A)
                                evidence_given_not_prior_event_name=evidence_given_not_prior_event_name # P(B|~A)
                            )
                        elif calc_type == "Binomial Distribution":
                            if prob_success_event_name_binomial is None:
                                st.error("Please select a variable for the probability of success (p).")
                                return
                            if num_successes_binomial > num_trials_binomial:
                                st.error("Number of successes (k) cannot be greater than the number of trials (n).")
                                return
                            result = calculate_probability(
                                variables_data,
                                calc_type,
                                prob_success_event_name=prob_success_event_name_binomial,
                                num_trials=num_trials_binomial,
                                num_successes=num_successes_binomial
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
                        results_text = f"Calculation Type: {calc_type}\nResult: {format_probability(result)}"
                        st.markdown(f"""
                        **Calculation Type:** {calc_type}  
                        **Result:** {format_probability(result)}
                        """)

                        # Add Copy and Share buttons
                        col1, col2 = st.columns(2)
                        with col1:
                            # Create button that sets text for clipboard API
                            st.button("📋 Copy Results",
                                      on_click=lambda: st.write(results_text))
                            # Add hidden element to store the text
                            st.markdown(f"""
                            <div class="stHidden">
                                <button id="copy-button" style="display:none"
                                   onclick="navigator.clipboard.writeText(`{results_text}`).then(
                                       () => {{ 
                                           const toastEvent = new CustomEvent('streamlit:showToast', {{ 
                                               detail: {{ kind: 'success', message: 'Results copied to clipboard!' }} 
                                           }}); 
                                           window.dispatchEvent(toastEvent);
                                       }}
                                   )">Copy</button>
                                <script>
                                    document.getElementById('copy-button').click();
                                </script>
                            </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            if st.button("🔗 Share Results"):
                                # Create shareable link with query parameters
                                query_params = {
                                    "calc_type": calc_type,
                                    "result": result,
                                    "variables": ",".join([f"{k}:{v}" for k, v in variables_data.items()])
                                }
                                # Use st.query_params.set to update URL
                                for k, v in query_params.items():
                                    st.experimental_set_query_params(**{k: v})
                                # Display success message
                                st.success("URL updated! Copy the URL from your browser to share these results.")

                        # Add formula display
                        st.markdown("### Formula Used")
                        if calc_type == "Joint Probability (AND)":
                            st.latex(r"P(A \cap B) = P(A) \times P(B)")
                        elif calc_type == "Union Probability (OR)":
                            st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
                        elif calc_type == "Conditional Probability":
                            st.latex(r"P(B|A) = \frac{P(A \cap B)}{P(A)}")
                        elif calc_type == "Bayes' Theorem":
                            st.latex(r"P(A|B) = \frac{P(B|A) \times P(A)}{P(B|A) \times P(A) + P(B|\neg A) \times P(\neg A)}")
                        elif calc_type == "Binomial Distribution":
                            st.latex(r"P(X=k) = C(n, k) \cdot p^k \cdot (1-p)^{n-k}")

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
        if st.button("New Calculation 🔄"):
            st.session_state.variables = []
            st.rerun()

if __name__ == "__main__":
    main()