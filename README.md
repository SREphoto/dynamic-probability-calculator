# Dynamic Probability Calculator

A Streamlit-powered web application for performing complex probability calculations with an interactive and user-friendly interface.

## Features

- **Interactive Variable Input**: Dynamic input fields tailored to the specific calculation type.
- **Comprehensive Probability Calculations**:
  - Joint Probability (AND)
  - Union Probability (OR)
  - Conditional Probability
  - Bayesian Inference
  - Expected Value
- **Statistical Distributions**:
  - Binomial Distribution
  - Poisson Distribution
  - Normal Distribution
- **Visualizations**: Interactive charts for probability distributions using Plotly.
- **History & Sharing**: Track past calculations and share results via URL.
- **Educational Tools**: View formulas and explanations for each calculation.

## Technologies Used

- Python 3.11
- Streamlit
- NumPy
- Pandas
- Plotly

## Setup and Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# OR if using uv
uv sync
```

3. Run the application:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Select Calculation Type**: Choose from the dropdown menu (e.g., Conditional Probability, Normal Distribution).
2. **Enter Parameters**: Input the required probabilities or values. The interface adapts to your selection.
3. **Calculate**: Click the "Calculate" button to view results.
4. **Visualize**: See interactive plots for distributions.
5. **History**: Access previous calculations in the sidebar.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
