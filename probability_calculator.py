
import numpy as np

def calculate_probability(variables, calc_type, event_A=None, event_B=None, n=None, k=None, p=None, rate=None):
    """
    Calculate probability based on the selected calculation type
    """
    if calc_type == "Joint Probability (AND)":
        return calculate_joint_probability(variables)
    elif calc_type == "Union Probability (OR)":
        return calculate_union_probability(variables)
    elif calc_type == "Conditional Probability":
        return calculate_conditional_probability(variables, event_A, event_B)
    elif calc_type == "Bayesian Inference":
        return calculate_bayesian_inference(variables, event_A, event_B)
    elif calc_type == "Binomial Probability":
        return calculate_binomial_probability(n, k, p)
    elif calc_type == "Poisson Distribution":
        return calculate_poisson_distribution(rate, k)
    elif calc_type == "Expected Value":
        return calculate_expected_value(variables)
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

def calculate_bayesian_inference(variables, event_A, event_B):
    """
    Calculate Bayesian inference P(B|A) = P(A|B) * P(B) / P(A)
    """
    p_a = variables.get(event_A)
    p_b = variables.get(event_B)
    p_a_given_b = variables.get(f"P({event_A}|{event_B})")

    if p_a is None or p_b is None or p_a_given_b is None:
        raise ValueError("Ensure probabilities for A, B, and P(A|B) are provided")

    if p_a == 0:
        raise ValueError("Probability of P(A) cannot be zero")

    return (p_a_given_b * p_b) / p_a

def calculate_binomial_probability(n, k, p):
    """
    Calculate binomial probability P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
    """
    if not (0 <= p <= 1):
        raise ValueError("Probability 'p' must be between 0 and 1")
    if k < 0 or k > n:
        raise ValueError("Number of successes 'k' must be between 0 and 'n'")

    from math import comb
    return comb(n, k) * (p**k) * ((1-p)**(n-k))

def calculate_poisson_distribution(rate, k):
    """
    Calculate Poisson distribution P(X=k) = (λ^k * e^-λ) / k!
    """
    if rate < 0:
        raise ValueError("Rate 'λ' must be non-negative")
    if k < 0:
        raise ValueError("Number of events 'k' must be non-negative")

    from math import exp, factorial
    return (rate**k * exp(-rate)) / factorial(k)

def calculate_expected_value(variables):
    """
    Calculate the expected value E[X] = Σ [x * P(x)]
    """
    total_expected_value = 0
    for value, prob in variables.items():
        total_expected_value += float(value) * prob
    return total_expected_value
