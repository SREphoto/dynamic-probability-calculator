
import math
from math import comb
import scipy.stats as stats

def calculate_lottery_probability(total_balls, balls_to_pick, bonus_balls=0, bonus_to_pick=0):
    """
    Calculate probability of winning a lottery (Jakpot).
    Powerball style: Match 5 of 69 (white) AND 1 of 26 (red).
    """
    try:
        white_prob = 1 / comb(total_balls, balls_to_pick)
        
        bonus_prob = 1.0
        if bonus_balls > 0 and bonus_to_pick > 0:
            bonus_prob = 1 / comb(bonus_balls, bonus_to_pick)
            
        return white_prob * bonus_prob
    except ValueError:
        return 0.0

def calculate_birthday_paradox(n_people):
    """
    Calculate probability that at least two people share a birthday in a group of n.
    P(shared) = 1 - P(all unique)
    """
    if n_people > 365:
        return 1.0
    if n_people <= 1:
        return 0.0
        
    prob_unique = 1.0
    for i in range(n_people):
        prob_unique *= (365 - i) / 365.0
        
    return 1 - prob_unique

def calculate_poker_outs(outs, cards_to_come):
    """
    Calculate probability of hitting an out.
    Approximate rule of 2/4 or exact. Using basic combinatorics here.
    """
    unknown_cards = 52 - 2 - 3 # Assumes Flop seen (Hero's 2 + Board's 3) usually 
    # But let's make it generic: 
    # If 1 card to come (River), unknown is approx 46.
    # If 2 cards to come (Turn+River), unknown is approx 47.
    
    # Generic approx for user ease:
    # 1 card (Turn or River): outs / unknown
    # 2 cards (Turn & River): 1 - (non-outs/unknown * non-outs-1/unknown-1)
    
    if cards_to_come not in [1, 2]:
        raise ValueError("Cards to come must be 1 or 2")
        
    unknown_cards = 47 # Standard assumption after flop (52 - 2 hole - 3 flop)
    
    if cards_to_come == 1:
        # P(Hit River) = outs / 46
        return outs / 46.0
    else:
        # P(Hit Turn or River) = 1 - P(Miss Both)
        # P(Miss Turn) = (47 - outs) / 47
        # P(Miss River | Miss Turn) = (46 - outs) / 46
        p_miss_turn = (47 - outs) / 47.0
        p_miss_river = (46 - outs) / 46.0
        return 1 - (p_miss_turn * p_miss_river)

def calculate_risk_of_ruin(win_rate, win_amount, loss_amount, bankroll):
    """
    Calculate Risk of Ruin using Kelly criterion approximation or simple Random Walk.
    RoR = ((1 - W)/(1 + W))^Units if win/loss amounts are equal.
    Here we generalize slightly for simple edge.
    
    Equation: ((1 - edge) / (1 + edge)) ^ bankroll_units
    Edge = P(Win) - P(Loss)
    Only valid if P(Win) > 0.5. If P(Win) <= 0.5, RoR is 1.0 (eventual rune).
    """
    # Simplyfy to binary outcome for this tool: Win 1 unit vs Lose 1 unit
    # Win rate p
    # q = 1 - p
    # if p <= 0.5, RoR = 1
    # if p > 0.5, RoR = (q/p)^bankroll
    
    if win_rate <= 0.5:
        return 1.0
        
    q = 1 - win_rate
    return (q / win_rate) ** bankroll

def calculate_ab_test_significance(conversions_a, visitors_a, conversions_b, visitors_b):
    """
    Calculate Two-Proportion Z-Test for A/B testing
    """
    p_a = conversions_a / visitors_a
    p_b = conversions_b / visitors_b
    
    # Pooled proportion
    p_pool = (conversions_a + conversions_b) / (visitors_a + visitors_b)
    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1/visitors_a + 1/visitors_b))
    
    if se_pool == 0:
        return 0.0, 1.0 # No variance
        
    z_score = (p_b - p_a) / se_pool
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score))) # Two-tailed
    
    confidence = 1 - p_value
    return p_value, confidence
