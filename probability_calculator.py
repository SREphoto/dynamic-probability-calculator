
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
    For two events: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
    For multiple events: Use the inclusion-exclusion principle
    """
    probabilities = list(variables.values())
    n = len(probabilities)
    
    if n == 0:
        return 0
    
    result = 0
    for k in range(1, n + 1):
        combinations = np.array(list(map(list, 
                              np.array(np.meshgrid(*[[0, 1]]*k)).T.reshape(-1, k))))
        term_sum = 0
        
        for combo in combinations[1:]:  # Skip the all-zeros combination
            indices = np.where(combo)[0]
            if len(indices) > 0:
                term = np.prod([probabilities[i] for i in indices])
                term_sum += term if len(indices) % 2 == 1 else -term
                
        result += term_sum
        
    return min(1, max(0, result))  # Ensure result is between 0 and 1

def calculate_conditional_probability(variables, event_A, event_B):
    """
    Calculate conditional probability P(B|A) = P(A ∩ B) / P(A)
    """
    if event_A not in variables or event_B not in variables:
        raise ValueError("Selected events not found in variables")
    
    p_a = variables[event_A]
    p_b = variables[event_B]
    
    if p_a == 0:
        raise ValueError("Probability of event A cannot be zero for conditional probability")
    
    # Assuming independence for simplicity
    p_intersection = p_a * p_b
    return p_intersection / p_a
