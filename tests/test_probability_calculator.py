import unittest
import math  # For math.comb in binomial if directly testing components
from probability_calculator import calculate_probability, calculate_bayes_theorem, calculate_binomial_distribution

class TestProbabilityCalculations(unittest.TestCase):

    def test_calculate_bayes_theorem_standard(self):
        variables = {'P(A)': 0.1, 'P(B|A)': 0.8, 'P(B|notA)': 0.2}
        # P(A|B) = (0.8 * 0.1) / (0.8 * 0.1 + 0.2 * 0.9)
        # P(A|B) = 0.08 / (0.08 + 0.18) = 0.08 / 0.26
        expected = 0.08 / 0.26
        result = calculate_bayes_theorem(variables, 'P(A)', 'P(B|A)', 'P(B|notA)')
        self.assertAlmostEqual(result, expected)

    def test_calculate_bayes_theorem_pa_zero(self):
        variables = {'P(A)': 0.0, 'P(B|A)': 0.8, 'P(B|notA)': 0.2}
        # P(A|B) = (0.8 * 0.0) / (0.8 * 0.0 + 0.2 * 1.0) = 0 / 0.2 = 0
        expected = 0.0
        result = calculate_bayes_theorem(variables, 'P(A)', 'P(B|A)', 'P(B|notA)')
        self.assertAlmostEqual(result, expected)

    def test_calculate_bayes_theorem_pa_one(self):
        variables = {'P(A)': 1.0, 'P(B|A)': 0.8, 'P(B|notA)': 0.2}
        # P(A|B) = (0.8 * 1.0) / (0.8 * 1.0 + 0.2 * 0.0) = 0.8 / 0.8 = 1
        expected = 1.0
        result = calculate_bayes_theorem(variables, 'P(A)', 'P(B|A)', 'P(B|notA)')
        self.assertAlmostEqual(result, expected)

    def test_calculate_bayes_theorem_denominator_zero(self):
        variables = {'P(A)': 0.5, 'P(B|A)': 0.0, 'P(B|notA)': 0.0}
        with self.assertRaisesRegex(ValueError, "Denominator P\\(B\\) cannot be zero"):
            calculate_bayes_theorem(variables, 'P(A)', 'P(B|A)', 'P(B|notA)')
    
    def test_calculate_bayes_theorem_missing_variable(self):
         variables = {'P(A)': 0.1, 'P(B|A)': 0.8} # Missing P(B|notA)
         with self.assertRaises(KeyError): # Expecting a KeyError when a variable is missing
             calculate_bayes_theorem(variables, 'P(A)', 'P(B|A)', 'P(B|notA)')


    def test_calculate_binomial_distribution_standard(self):
        variables = {'p_success': 0.5}
        # C(10, 3) * (0.5^3) * (0.5^7)
        # 120 * 0.125 * 0.0078125
        expected = 120 * (0.5**3) * (0.5**7)
        result = calculate_binomial_distribution(variables, 'p_success', 10, 3)
        self.assertAlmostEqual(result, expected)

    def test_calculate_binomial_distribution_k_zero(self):
        variables = {'p_success': 0.3}
        # C(5, 0) * (0.3^0) * (0.7^5) = 1 * 1 * 0.7^5
        expected = (0.7**5)
        result = calculate_binomial_distribution(variables, 'p_success', 5, 0)
        self.assertAlmostEqual(result, expected)

    def test_calculate_binomial_distribution_k_equals_n(self):
        variables = {'p_success': 0.6}
        # C(4, 4) * (0.6^4) * (0.4^0) = 1 * 0.6^4 * 1
        expected = (0.6**4)
        result = calculate_binomial_distribution(variables, 'p_success', 4, 4)
        self.assertAlmostEqual(result, expected)

    def test_calculate_binomial_distribution_p_zero(self):
        variables = {'p_success': 0.0}
        # k=0: C(n,0)*0^0*1^n -> 1 (0^0 is 1 in this context)
        # k>0: C(n,k)*0^k*1^(n-k) -> 0
        result_k_zero = calculate_binomial_distribution(variables, 'p_success', 5, 0)
        self.assertAlmostEqual(result_k_zero, 1.0)
        result_k_gt_zero = calculate_binomial_distribution(variables, 'p_success', 5, 1)
        self.assertAlmostEqual(result_k_gt_zero, 0.0)

    def test_calculate_binomial_distribution_p_one(self):
        variables = {'p_success': 1.0}
        # k=n: C(n,n)*1^n*0^0 -> 1
        # k<n: C(n,k)*1^k*0^(n-k) -> 0
        result_k_equals_n = calculate_binomial_distribution(variables, 'p_success', 5, 5)
        self.assertAlmostEqual(result_k_equals_n, 1.0)
        result_k_lt_n = calculate_binomial_distribution(variables, 'p_success', 5, 4)
        self.assertAlmostEqual(result_k_lt_n, 0.0)

    def test_calculate_binomial_distribution_n_zero(self):
        variables = {'p_success': 0.5}
        # C(0, 0) * (0.5^0) * (0.5^0) = 1
        expected = 1.0
        result = calculate_binomial_distribution(variables, 'p_success', 0, 0)
        self.assertAlmostEqual(result, expected)

    def test_calculate_binomial_distribution_invalid_k_greater_than_n(self):
        variables = {'p_success': 0.5}
        with self.assertRaisesRegex(ValueError, "Number of successes cannot exceed number of trials"):
            calculate_binomial_distribution(variables, 'p_success', 5, 6)
    
    def test_calculate_binomial_distribution_invalid_p_too_low(self):
         variables = {'p_success': -0.1}
         with self.assertRaisesRegex(ValueError, "Probability of success must be between 0 and 1"):
             calculate_binomial_distribution(variables, 'p_success', 5, 2)

    def test_calculate_binomial_distribution_invalid_p_too_high(self):
         variables = {'p_success': 1.1}
         with self.assertRaisesRegex(ValueError, "Probability of success must be between 0 and 1"):
             calculate_binomial_distribution(variables, 'p_success', 5, 2)
    
    def test_calculate_binomial_distribution_missing_variable(self):
         variables = {} # Missing p_success
         with self.assertRaises(KeyError):
             calculate_binomial_distribution(variables, 'p_success', 5, 2)

    # Example of testing through the main calculate_probability dispatcher
    def test_calculate_probability_bayes_theorem(self):
        variables = {'P(A)': 0.1, 'P(B|A)': 0.8, 'P(B|notA)': 0.2}
        expected = 0.08 / 0.26 # From previous manual calculation
        result = calculate_probability(variables, "Bayes' Theorem", 
                                       event_A='P(A)', event_B='P(B|A)', 
                                       evidence_given_not_prior_event_name='P(B|notA)')
        self.assertAlmostEqual(result, expected)

    def test_calculate_probability_binomial_distribution(self):
        variables = {'p': 0.5}
        expected = 120 * (0.5**3) * (0.5**7) # From previous manual calculation
        result = calculate_probability(variables, "Binomial Distribution",
                                       prob_success_event_name='p', 
                                       num_trials=10, num_successes=3)
        self.assertAlmostEqual(result, expected)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
