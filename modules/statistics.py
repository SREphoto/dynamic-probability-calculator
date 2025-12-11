
import numpy as np
import scipy.stats as stats

def calculate_descriptive_stats(data):
    """
    Calculate Mean, Median, Mode, Variance, Skewness
    """
    if len(data) == 0:
        return {}
    
    return {
        "Mean": np.mean(data),
        "Median": np.median(data),
        "Mode": float(stats.mode(data, keepdims=True)[0][0]),
        "Variance": np.var(data, ddof=1), # Sample variance
        "Std Dev": np.std(data, ddof=1),
        "Skewness": stats.skew(data),
        "Min": np.min(data),
        "Max": np.max(data)
    }

def perform_z_test(data, population_mean, population_std):
    """
    Perform One-Sample Z-Test
    """
    n = len(data)
    sample_mean = np.mean(data)
    standard_error = population_std / np.sqrt(n)
    z_score = (sample_mean - population_mean) / standard_error
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score))) # Two-tailed
    
    return {
        "Sample Mean": sample_mean,
        "Z-Score": z_score,
        "P-Value": p_value
    }

def perform_t_test(data, population_mean):
    """
    Perform One-Sample T-Test
    """
    t_stat, p_value = stats.ttest_1samp(data, population_mean)
    return {
        "T-Statistic": t_stat,
        "P-Value": p_value
    }
