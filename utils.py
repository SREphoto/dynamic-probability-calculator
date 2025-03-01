def validate_input(variables):
    """
    Validate that all input probabilities are between 0 and 1
    """
    return all(0 <= value <= 1 for value in variables.values())

def format_probability(probability):
    """
    Format probability for display with improved readability
    """
    return f"{probability:.4f} ({probability*100:.1f}%)"
