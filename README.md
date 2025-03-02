# Dynamic Probability Calculator

A Streamlit-based web application for calculating various probability types including:
- Joint Probability (AND)
- Union Probability (OR)
- Conditional Probability

## Features
- Add/remove multiple probability variables
- Interactive and user-friendly interface
- Real-time calculation updates
- View calculation history
- Copy and share results via URL
- Responsive design

## Technology Stack
- **Frontend & Backend**: Streamlit
- **Data Processing**: NumPy, Pandas
- **Language**: Python 3.x

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dynamic-probability-calculator.git
cd dynamic-probability-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## Usage

1. Launch the application
2. Click "Add Variable" to create new probability variables
3. Enter values between 0 and 1 for each variable
4. Select the type of probability calculation:
   - Joint Probability (AND)
   - Union Probability (OR)
   - Conditional Probability
5. Click "Calculate" to see results
6. View calculation history in the sidebar

## Project Structure
```
├── main.py               # Main application file
├── probability_calculator.py  # Core calculation logic
├── utils.py             # Utility functions
├── test_app.py         # Test suite
└── requirements.txt    # Project dependencies
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.