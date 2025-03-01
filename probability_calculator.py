
import numpy as np

def calculate_probability(variables, calc_type, event_A=None, event_B=None):
    """
    Calculate probability based on the selected calculation type
    """
    if calc_type == "Joint Probability (AND)":
        return calculate_joint_probability(variables)
    elif calc_type == "Union Probability (OR)":
        return calculate_union_probability(variables)
    elif calc_type == "Conditional Probability":
        return calculate_conditional_probability(variables, event_A, event_B)
    else:
        raise ValueError("Invalid calculation type")

def calculate_joint_probability(variables):
    """
    Calculate the joint probability (AND) of all variables
    P(A ∩ B ∩ C...) = P(A) × P(B) × P(C)...
    """
    probabilities = list(variables.values())
    return np.prod(probabilities)

def calculate_union_probability(variables):
    """
    Calculate the union probability (OR) of all variables
    P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
    For multiple variables, this extends to the inclusion-exclusion principle
    """
    probabilities = list(variables.values())
    n = len(probabilities)
    
    # Initialize result with sum of individual probabilities
    result = sum(probabilities)
    
    # Subtract overlaps
    for i in range(n):
        for j in range(i+1, n):
            result -= probabilities[i] * probabilities[j]
    
    # For more than 2 variables, adjust with inclusion-exclusion principle
    if n > 2:
        # Add back triple intersections
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    result += probabilities[i] * probabilities[j] * probabilities[k]
    
    # Continue pattern for higher orders if needed
    
    # Ensure probability is not greater than 1
    return min(result, 1.0)

def calculate_conditional_probability(variables, event_A, event_B):
    """
    Calculate conditional probability: P(B|A) = P(A ∩ B) / P(A)
    """
    if event_A not in variables or event_B not in variables:
        raise ValueError("Events must be defined in variables")
    
    # Get probabilities
    p_A = variables[event_A]
    p_B = variables[event_B]
    
    # Calculate joint probability (assuming independence for simplicity)
    p_A_and_B = p_A * p_B
    
    # Calculate conditional probability
    if p_A == 0:
        raise ValueError("Cannot condition on event with zero probability")
    
    return p_A_and_B / p_A
