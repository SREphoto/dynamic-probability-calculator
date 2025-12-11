
import numpy as np

def calculate_joint_probability(variables):
    """
    Calculate the joint probability (AND) of all variables
    P(A ∩ B ∩ C...) = P(A) × P(B) × P(C)... (Assuming Independence)
    """
    probabilities = list(variables.values())
    return np.prod(probabilities)

def calculate_union_probability(variables):
    """
    Calculate the union probability (OR) of all variables
    P(A ∪ B ∪ ...) = 1 - P(A' ∩ B' ∩ ...)
    """
    probabilities = list(variables.values())
    if not probabilities:
        return 0
    
    # Calculate probability of NONE occurring
    prob_none = np.prod([1 - p for p in probabilities])
    
    # Result is 1 - probability of none
    return 1 - prob_none

def calculate_conditional_probability(variables, event_A, event_B, intersection_prob=None):
    """
    Calculate conditional probability P(B|A) = P(A ∩ B) / P(A)
    """
    if event_A not in variables:
        raise ValueError(f"Event {event_A} not found")
    
    p_a = variables[event_A]
    
    if p_a == 0:
        raise ValueError("Probability of event A cannot be zero for conditional probability")

    if intersection_prob is not None:
        p_intersection = intersection_prob
    else:
        # Fallback to independence if intersection not provided
        # P(A ∩ B) = P(A) * P(B)
        if event_B not in variables:
             raise ValueError(f"Event {event_B} not found")
        p_b = variables[event_B]
        p_intersection = p_a * p_b
    
    return p_intersection / p_a

def calculate_bayesian_inference(variables, event_A, event_B):
    """
    Calculate Bayesian inference P(H|E) = P(E|H) * P(H) / P(E)
    """
    p_h = variables.get(event_A) # Prior P(H)
    p_e = variables.get(event_B) # Marginal P(E)
    
    likelihood_key = f"P({event_B}|{event_A})"
    p_e_given_h = variables.get(likelihood_key)

    if p_h is None or p_e is None or p_e_given_h is None:
        raise ValueError(f"Missing probabilities. Need P({event_A}), P({event_B}), and P({event_B}|{event_A})")

    if p_e == 0:
        raise ValueError(f"Probability of evidence P({event_B}) cannot be zero")

    return (p_e_given_h * p_h) / p_e

def calculate_expected_value(variables):
    """
    Calculate the expected value E[X] = Σ [x * P(x)]
    """
    total_expected_value = 0
    for name, prob in variables.items():
        try:
            val = float(name)
            total_expected_value += val * prob
        except ValueError:
             raise ValueError(f"Variable name '{name}' is not a number. For Expected Value, variable names must be the numeric values of the outcomes.")
             
    return total_expected_value
