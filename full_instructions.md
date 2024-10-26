# Daleview Pool Financial Calculator

## Overview
The Daleview Pool Financial Calculator is an interactive web application that helps model and visualize the financial implications of the pool renovation project. It allows stakeholders to explore different scenarios for membership, revenue, financing options, and assess long-term financial sustainability.

## Features
- **Interactive Financial Modeling**
  - Member count and dues projections
  - Multiple revenue stream analysis
  - Customizable project costs
  - Flexible financing options including The Footnote (member bonds) and commercial loans
  - One-time member assessments modeling

- **Comprehensive Visualizations**
  - Project funding source breakdown
  - 20-year financial projections
  - Operating surplus/deficit analysis
  - Revenue and expense trends

- **Economic Analysis**
  - Inflation-adjusted projections
  - Debt service calculations
  - Operating cost analysis
  - Long-term sustainability metrics

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup
1. Clone the repository:
```bash
git clone [repository-url]
cd daleview-finance
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Required Packages
Create a `requirements.txt` file with the following contents:
```
streamlit
pandas
plotly
numpy
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the left sidebar to adjust:
   - Economic assumptions
   - Future revenue projections
   - Project costs
   - Financing options

4. View results in real-time on the right side of the screen:
   - Operating financial impact
   - Project funding breakdown
   - 20-year projections

## Current Operating Assumptions
- Members: 325
- Annual Dues Revenue: $226,760
- Swim Team Revenue: $45,000
- Winter Swim Revenue: $71,000
- Current Operating Expenses: $347,000

## Financial Terms

### The Footnote (Membership Bond Program)
- Term: 5-15 years (default 10)
- Interest rates: 3-8% (default 5.5%)
- Individual bond amounts: $1,000-$10,000
- Optional participation

### Commercial Loan
- Term: 10-30 years (default 20)
- Interest rates: 5-12% (default 8.5%)
- Covers remaining project costs after assessments and bonds

## Data Visualization
The application provides several ways to view and analyze the financial data:
1. Operating Financial Impact metrics
2. Project Funding Sources pie chart
3. 20-Year Financial Projections table
4. Trend visualization graph

## Contributing
To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Known Limitations
- All projections assume fixed interest rates
- Operating expenses are inflated uniformly
- Revenue streams are projected linearly with inflation
- Member counts are assumed to be stable within each scenario

## Support
For questions or issues:
- Submit an issue in the repository
- Contact the development team at [contact information]

## License
[Specify license information]

## Acknowledgments
- Daleview Pool Board of Directors
- Financial Planning Committee
- Development Team