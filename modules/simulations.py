
import random
import numpy as np
from collections import Counter

def simulate_dice_rolls(num_dice, num_rolls):
    """
    Simulate rolling N dice K times.
    Returns: list of sums
    """
    results = []
    for _ in range(num_rolls):
        roll_sum = sum(random.randint(1, 6) for _ in range(num_dice))
        results.append(roll_sum)
    return results

def simulate_coin_flips(num_coins, num_flips):
    """
    Simulate flipping N coins K times.
    Returns: list of heads counts
    """
    # 0 = Tails, 1 = Heads
    results = np.random.binomial(num_coins, 0.5, num_flips)
    return results

def simulate_card_draws(num_draws, hand_size=5):
    """
    Simulate drawing hands from a deck.
    Simple simulation returning random card values for now.
    """
    # Simplified: Just drawing values 1-13 (Ace-King)
    results = []
    deck = list(range(1, 14)) * 4
    for _ in range(num_draws):
        hand = random.sample(deck, hand_size)
        results.append(sum(hand)) # simplified analytic
    return results
