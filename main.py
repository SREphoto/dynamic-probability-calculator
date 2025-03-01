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
            1. Add variables using the 'Add Variable' button
            2. Enter values for each variable
            3. Select calculation type
            4. View results
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
                    'Probability',
                    min_value=0.0,
                    max_value=1.0,
                    value=float(var['value']),
                    key=f'value_{idx}',
                    format="%.4f"
                )
                var['value'] = new_value
                variables_data[new_name] = new_value

            with col3:
                # Use horizontal layout for buttons with equal width
                remove_btn, add_btn = st.columns(2)
                with remove_btn:
                    if st.button('Remove ❌', key=f'remove_{idx}', use_container_width=True):
                        st.session_state.variables.pop(idx)
                        st.rerun()
                with add_btn:
                    if st.button('Add ➕', key=f'add_another_{idx}', use_container_width=True):
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
        if st.button("New Calculation 🔄"):
            st.session_state.variables = []
            st.rerun()

if __name__ == "__main__":
    main()