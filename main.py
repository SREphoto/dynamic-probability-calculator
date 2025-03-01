
import streamlit as st
import numpy as np
import pandas as pd
from probability_calculator import calculate_probability
from utils import validate_input, format_probability

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Dynamic Probability Calculator",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    try:
        local_css(".streamlit/style.css")
    except:
        st.write("Custom styling file not found.")

    # Initialize session state for variables and past calculations
    if 'variables' not in st.session_state:
        st.session_state.variables = []
    if 'past_calculations' not in st.session_state:
        st.session_state.past_calculations = []
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "calculator"

    # App header with custom styling
    st.markdown("<h1 class='main-title'>Dynamic Probability Calculator 🎲</h1>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["Calculator", "History"])
    
    with tab1:
        # Main calculator section
        main_container = st.container()
        
        with main_container:
            # Instructions with cleaner styling
            st.markdown("<div class='instructions'>", unsafe_allow_html=True)
            st.markdown("""
            ### How to use this calculator:
            1. Add variables using the 'Add Variable' button
            2. Enter values for each variable
            3. Select calculation type
            4. View results
            """)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Variable section with add button
            st.subheader("Variables")
            col1, col2 = st.columns([5, 1])
            with col2:
                if st.button('Add Variable ➕', key="add_var_btn", use_container_width=True):
                    st.session_state.variables.append({
                        'name': f'Variable {len(st.session_state.variables) + 1}',
                        'value': 0.5
                    })
            
            # Display variables in cards
            variables_data = {}
            for idx, var in enumerate(st.session_state.variables):
                st.markdown(f"<div class='variable-card'>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    new_name = st.text_input(
                        'Variable Name',
                        value=var['name'],
                        key=f'name_{idx}',
                        placeholder="Enter variable name"
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
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button('Remove', key=f'remove_{idx}', use_container_width=True):
                        st.session_state.variables.pop(idx)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Calculation options
            if st.session_state.variables:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader("Calculation Options")
                calc_type = st.selectbox(
                    "Select Probability Calculation",
                    ["Joint Probability (AND)",
                     "Union Probability (OR)",
                     "Conditional Probability"]
                )
                
                # Conditional probability options
                cond_options = st.container()
                with cond_options:
                    event_A, event_B = None, None
                    if calc_type == "Conditional Probability" and len(st.session_state.variables) >= 2:
                        col1, col2 = st.columns(2)
                        with col1:
                            event_A = st.selectbox("Select Event A (Given)", 
                                                [var['name'] for var in st.session_state.variables])
                        with col2:
                            event_B = st.selectbox("Select Event B (Target)", 
                                                [var['name'] for var in st.session_state.variables 
                                                 if var['name'] != event_A])
                
                # Calculate button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button('Calculate Probability', key="calc_btn", use_container_width=True, type="primary"):
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
                            
                            # Display results in a nicer format
                            st.markdown("<div class='results-section'>", unsafe_allow_html=True)
                            st.subheader("Results 📊")
                            
                            result_cols = st.columns([3, 1])
                            with result_cols[0]:
                                st.metric(
                                    label=f"{calc_type}",
                                    value=f"{format_probability(result)}"
                                )
                            
                            # Add button to show formula with better styling
                            with result_cols[1]:
                                st.markdown("<br>", unsafe_allow_html=True)
                                if st.button('Show Formula 📐', key="formula_btn"):
                                    st.markdown("### Formula Used")
                                    if calc_type == "Joint Probability (AND)":
                                        st.latex(r"P(A \cap B) = P(A) \times P(B)")
                                    elif calc_type == "Union Probability (OR)":
                                        st.latex(r"P(A \cup B) = P(A) + P(B) - P(A \cap B)")
                                    else:
                                        st.latex(r"P(B|A) = \frac{P(A \cap B)}{P(A)}")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        except Exception as e:
                            st.error(f"Calculation Error: {str(e)}")
                    else:
                        st.error("Please ensure all probabilities are between 0 and 1.")
            else:
                st.info("Add variables to start calculating probabilities!")
                
        # New calculation button
        if st.session_state.variables:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("New Calculation 🔄", key="new_calc", use_container_width=True):
                st.session_state.variables = []
                st.rerun()
    
    with tab2:
        # History section
        st.subheader("Calculation History")
        if st.session_state.past_calculations:
            for calc in reversed(st.session_state.past_calculations):
                with st.expander(f"{calc['type']} - Result: {format_probability(calc['result'])}"):
                    st.write("Variables used:")
                    # Create a nicer display of variables
                    var_data = [[name, format_probability(value)] for name, value in calc['variables'].items()]
                    st.table(pd.DataFrame(var_data, columns=["Variable", "Value"]))
                    
                    if st.button("Use Result as New Variable", key=f"use_{calc['id']}"):
                        st.session_state.variables.append({
                            'name': f"Result_{calc['type']}_{calc['id']}",
                            'value': calc['result']
                        })
                        st.rerun()
        else:
            st.info("No past calculations yet.")
    
    # Footer
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("Dynamic Probability Calculator | Created with Streamlit")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
