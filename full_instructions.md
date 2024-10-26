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

## Detailed Calculation Methodologies

### Revenue Calculations

#### Membership Revenue
```python
future_dues_revenue = future_members * future_avg_dues
```
- Base calculation before inflation adjustments
- Assumes uniform dues structure across membership

#### Total Revenue
```python
future_total_revenue = future_dues_revenue + future_swim_team + future_winter_swim + future_other
```
- Combines all revenue streams
- Each component can be independently adjusted
- Used as base for inflation projections

### Financing Calculations

#### Member Assessments
```python
total_assessment = current_members * assessment_per_member
```
- One-time contribution from existing members
- Reduces amount needed from other funding sources
- Collected upfront to reduce borrowing needs

#### The Footnote (Membership Bond Program)
```python
total_bond_funding = bond_participants * avg_bond_amount
monthly_rate = bond_interest_rate / (12 * 100)
n_payments = bond_term * 12

monthly_bond_payment = total_bond_funding * (monthly_rate * (1 + monthly_rate)**n_payments) / 
                      ((1 + monthly_rate)**n_payments - 1)
annual_bond_payment = monthly_bond_payment * 12
total_bond_cost = annual_bond_payment * bond_term
```
- Uses standard amortization formula
- Fixed interest rate over term
- Payments calculated monthly but analyzed annually
- Term typically shorter than commercial loan (5-15 years)

#### Commercial Loan
```python
remaining_to_finance = total_cost - total_bond_funding - total_assessment
monthly_rate = commercial_interest_rate / (12 * 100)
n_payments = commercial_term * 12

monthly_loan_payment = remaining_to_finance * (monthly_rate * (1 + monthly_rate)**n_payments) / 
                      ((1 + monthly_rate)**n_payments - 1)
annual_loan_payment = monthly_loan_payment * 12
total_loan_cost = annual_loan_payment * commercial_term
```
- Finances remaining project costs
- Uses same amortization formula as bonds
- Typically longer term (10-30 years)
- Higher interest rate than bonds

### Time-Based Projections

#### Inflation Adjustments
```python
inflation_factor = (1 + inflation_rate/100) ** year
projected_revenue = future_total_revenue * inflation_factor
projected_expenses = current_expenses * inflation_factor
```
- Compound inflation applied to both revenue and expenses
- Debt service remains constant (fixed-rate assumption)
- Applied uniformly across all operating costs

#### Year-Specific Calculations
```python
year_bond_payment = annual_bond_payment if year < bond_term else 0
year_loan_payment = annual_loan_payment if year < commercial_term else 0
year_debt_service = year_bond_payment + year_loan_payment

total_costs = projected_expenses + year_debt_service
debt_service_percentage = (year_debt_service / total_costs) * 100
operating_surplus = projected_revenue - total_costs
```
- Accounts for bond term completion
- Tracks debt service as percentage of total costs
- Calculates real operating surplus/deficit

### Financial Health Metrics

#### Operating Surplus/Deficit
```python
current_surplus = current_total_revenue - current_expenses
future_surplus = future_total_revenue - current_expenses - total_annual_debt_service
```
- Measures basic operational sustainability
- Includes debt service impact
- Used for initial viability assessment

#### Debt Service Coverage
```python
debt_service_percentage = (year_debt_service / total_costs) * 100
```
- Tracks debt burden over time
- Key metric for financial health
- Helps identify unsustainable scenarios

### Key Financial Indicators

#### Project Funding Mix
- Tracks proportion of funding from each source:
  * Member assessments
  * The Footnote (bonds)
  * Commercial loan
- Used to optimize funding strategy
- Helps balance member contribution vs external financing

#### Long-term Sustainability Metrics
- 20-year projections at 5-year intervals
- Tracks key metrics:
  * Revenue growth with inflation
  * Operating expense inflation
  * Debt service burden
  * Operating surplus/deficit trends
- Used for strategic planning and risk assessment

### Assumptions and Limitations

1. **Fixed Rate Assumptions**
   - All debt instruments assume fixed rates
   - No refinancing scenarios included
   - No variable rate options modeled

2. **Revenue Projections**
   - Linear membership growth/decline
   - Uniform inflation across revenue streams
   - No seasonal variation modeling

3. **Expense Projections**
   - Uniform inflation across all expense categories
   - No major maintenance/replacement costs included
   - Operating costs assumed to scale linearly

4. **Timing Assumptions**
   - All financing starts simultaneously
   - Assessment collection assumed upfront
   - No construction period modeling

These calculation methodologies provide a framework for financial decision-making while acknowledging the inherent uncertainties in long-term projections. The model is designed to be conservative in its estimates while providing flexibility to explore different scenarios.
