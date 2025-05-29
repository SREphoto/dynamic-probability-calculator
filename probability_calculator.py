
import numpy as np
import math

def calculate_probability(variables, calc_type, event_A=None, event_B=None, **kwargs):
    """
    Calculate probability based on the selected calculation type
    """
    if calc_type == "Joint Probability (AND)":
        return calculate_joint_probability(variables)
    elif calc_type == "Union Probability (OR)":
        return calculate_union_probability(variables)
    elif calc_type == "Conditional Probability":
        return calculate_conditional_probability(variables, event_A, event_B)
    elif calc_type == "Bayes' Theorem":
        return calculate_bayes_theorem(variables, event_A, event_B, kwargs.get('evidence_given_not_prior_event_name'))
    elif calc_type == "Binomial Distribution":
        return calculate_binomial_distribution(
            variables,
            kwargs.get('prob_success_event_name'),
            kwargs.get('num_trials'),
            kwargs.get('num_successes')
        )
    else:
        raise ValueError("Invalid calculation type")

def calculate_binomial_distribution(variables, prob_success_event_name, num_trials, num_successes):
    """
    Calculate the Binomial Distribution P(X=k) = C(n, k) * p^k * (1-p)^(n-k)
    """
    # Attempt to access p first, which will raise KeyError if prob_success_event_name is not in variables
    # or if prob_success_event_name is None/empty and then used as a key.
    # This aligns with the test expecting KeyError for missing variable.
    if not prob_success_event_name:
        raise ValueError("Probability of success event name must be provided.")
    
    p = variables[prob_success_event_name] # This will raise KeyError if the name is not in variables

    if num_trials is None or not isinstance(num_trials, int) or num_trials < 0:
        raise ValueError("Number of trials (n) must be a non-negative integer.")
    if num_successes is None or not isinstance(num_successes, int) or num_successes < 0:
        raise ValueError("Number of successes (k) must be a non-negative integer.")

    p = variables[prob_success_event_name]

    if not (0 <= p <= 1):
        raise ValueError("Probability of success must be between 0 and 1")
    if num_successes > num_trials:
        raise ValueError("Number of successes cannot exceed number of trials")

    combinations = math.comb(num_trials, num_successes)
    result = combinations * (p**num_successes) * ((1-p)**(num_trials - num_successes))
    return result

def calculate_bayes_theorem(variables, prior_event_name, evidence_given_prior_event_name, evidence_given_not_prior_event_name):
    """
    Calculate P(A|B) using Bayes' Theorem: P(A|B) = (P(B|A) * P(A)) / P(B)
    where P(B) = P(B|A) * P(A) + P(B|¬A) * P(¬A)
    """
    p_a = variables[prior_event_name]
    p_b_given_a = variables[evidence_given_prior_event_name]
    p_b_given_not_a = variables[evidence_given_not_prior_event_name]

    p_not_a = 1 - p_a

    p_b = (p_b_given_a * p_a) + (p_b_given_not_a * p_not_a)

    if p_b == 0:
        raise ValueError("Denominator P(B) cannot be zero")

    p_a_given_b = (p_b_given_a * p_a) / p_b
    return p_a_given_b

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
