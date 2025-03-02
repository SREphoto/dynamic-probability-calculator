# Dynamic Probability Calculator

A Streamlit-powered web application for performing complex probability calculations with an interactive and user-friendly interface.

## Features

- Interactive variable input system
- Multiple probability calculation types:
  - Joint Probability (AND)
  - Union Probability (OR)
  - Conditional Probability
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
