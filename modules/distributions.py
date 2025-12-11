
from math import comb, exp, factorial, sqrt, pi, erf

def calculate_binomial_probability(n, k, p):
    """
    Calculate binomial probability P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
    """
    if not (0 <= p <= 1):
        raise ValueError("Probability 'p' must be between 0 and 1")
    if k < 0 or k > n:
        raise ValueError("Number of successes 'k' must be between 0 and 'n'")

    return comb(n, k) * (p**k) * ((1-p)**(n-k))

def calculate_poisson_distribution(rate, k):
    """
    Calculate Poisson distribution P(X=k) = (λ^k * e^-λ) / k!
    """
    if rate < 0:
        raise ValueError("Rate 'λ' must be non-negative")
    if k < 0:
        raise ValueError("Number of events 'k' must be non-negative")

    return (rate**k * exp(-rate)) / factorial(k)

def calculate_normal_distribution(mean, std_dev, lower, upper):
    """
    Calculate probability P(lower <= X <= upper) for Normal Distribution
    """
    if std_dev <= 0:
        raise ValueError("Standard deviation must be positive")
    
    def cdf(x):
        return 0.5 * (1 + erf((x - mean) / (std_dev * sqrt(2))))
    
    return cdf(upper) - cdf(lower)

def calculate_geometric_distribution(p, k):
    """
    Calculate Geometric Distribution P(X=k) = (1-p)^(k-1) * p
    Probability of success on the k-th trial.
    """
    if not (0 < p <= 1):
        raise ValueError("Probability 'p' must be in (0, 1]")
    if k < 1:
        raise ValueError("Number of trials 'k' must be >= 1")
        
    return ((1 - p)**(k - 1)) * p

def calculate_exponential_distribution(rate, lower, upper):
    """
    Calculate probability P(lower <= X <= upper) for Exponential Distribution
    CDF = 1 - e^(-λx)
    """
    if rate <= 0:
        raise ValueError("Rate 'λ' must be positive")
    
    def cdf(x):
        if x < 0: return 0
        return 1 - exp(-rate * x)
        
    return cdf(upper) - cdf(lower)
