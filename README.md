# Dynamic Probability Calculator

A Streamlit-powered web application for performing complex probability calculations with an interactive and user-friendly interface.

## Features

- Interactive variable input system
- Multiple probability calculation types:
  - Joint Probability (AND): Calculates P(A ∩ B ∩ C...).
  - Union Probability (OR): Calculates P(A ∪ B ∪ C...).
  - Conditional Probability: Calculates P(B|A).
  - **Bayes' Theorem:**
    - Calculates the probability of an event based on prior knowledge of conditions that might be related to the event (P(A|B)).
    - Requires three probabilities selected from your defined variables:
      - P(A): The prior probability of event A.
      - P(B|A): The probability of observing evidence B if event A is true.
      - P(B|¬A): The probability of observing evidence B if event A is false.
  - **Binomial Distribution:**
    - Calculates the probability of achieving a specific number of successes (`k`) in a fixed number of independent trials (`n`), given a constant probability of success (`p`) for each trial.
    - Requires:
      - Probability of Success (p): Select one of your defined variables.
      - Number of Trials (n): Enter the total number of trials.
      - Number of Successes (k): Enter the specific number of successes you are interested in.
- Calculation history tracking
- Result sharing functionality
- Dynamic formula display
- User-friendly interface with real-time updates

## Technologies Used

- Python 3.11
- Streamlit
- NumPy
- Pandas

## Setup and Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Add variables using the "Add Variable" button
2. Enter variable names and probability values (between 0 and 1)
3. Select the type of probability calculation
4. Click "Calculate Probability" to see the results
5. View calculation history in the sidebar
6. Share results using the share button

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
