"""
Main application file for the Daleview Pool Financial Calculator.
Handles the overall application flow and layout.
"""
import streamlit as st
import pandas as pd
from src import config, styles
from src.calculations import FinancingInputs, YearMetricsInputs, calculate_financing_metrics, calculate_year_metrics
from src.components import inputs, metrics, charts

# Set page config must be the first Streamlit command
st.set_page_config(page_title="Daleview Pool Financial Calculator", layout="wide")

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Please enter the password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.stop()
    
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "Please enter the password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        st.stop()
    
    return True

# Check password before showing anything else
check_password()

# Only show the app content after successful authentication
st.title("Daleview Pool Renovation Financial Model")

# Apply custom styles
st.markdown(styles.STYLES, unsafe_allow_html=True)

# Create main layout
left_col, right_col = st.columns([1, 2])

# Left column - Input sections
with left_col:
    # Render input sections and collect their returns
    inputs.render_current_revenue_breakdown()
    inflation_rate = inputs.render_economic_assumptions()
    
    revenue_model = inputs.render_future_revenue_model()
    if revenue_model is None:
        st.stop()  # Stop if revenue model validation failed
        
    future_total_revenue = (
        revenue_model['members'] * revenue_model['avg_dues'] +
        revenue_model['swim_team'] + 
        revenue_model['winter_swim'] + 
        revenue_model['other']
    )
    
    total_cost, assessment_per_member, total_assessment = inputs.render_project_cost_section()
    financing_options = inputs.render_financing_options(revenue_model['members'])

# Calculate financing metrics using new dataclass
total_bond_funding = financing_options['bond_participants'] * financing_options['avg_bond_amount']
remaining_to_finance = total_cost - total_bond_funding - total_assessment

financing_inputs = FinancingInputs(
    total_bond_funding=total_bond_funding,
    bond_term=financing_options['bond_term'],
    bond_interest_rate=financing_options['bond_interest_rate'],
    remaining_to_finance=remaining_to_finance,
    commercial_term=financing_options['commercial_term'],
    commercial_interest_rate=financing_options['commercial_interest_rate']
)
finance_metrics = calculate_financing_metrics(financing_inputs)

# Right column - Results and visualizations
with right_col:
    # Calculate key metrics
    current_surplus = (config.get_operating_metric('TOTAL_REVENUE') - 
                      config.get_operating_metric('EXPENSES'))
    future_surplus = (future_total_revenue - 
                     config.get_operating_metric('EXPENSES') - 
                     finance_metrics['total_annual_debt_service'])
    
    # Render financial impact section
    metrics.render_financial_impact_metrics(
        current_surplus=current_surplus,
        total_cost_of_borrowing=finance_metrics['total_cost_of_borrowing'],
        total_annual_debt_service=finance_metrics['total_annual_debt_service'],
        future_surplus=future_surplus,
        total_cost=total_cost
    )
    
    # Calculate and render 5-year projection
    year_5_inputs = YearMetricsInputs(
    year=5,
    future_total_revenue=future_total_revenue,
    inflation_rate=inflation_rate,
    current_expenses=config.get_operating_metric('EXPENSES'),
    annual_bond_payment=finance_metrics['annual_bond_payment'],
    annual_loan_payment=finance_metrics['annual_loan_payment'],
    bond_term=financing_options['bond_term'],
    commercial_term=financing_options['commercial_term']
)
    year_5_metrics = calculate_year_metrics(year_5_inputs)
    metrics.render_warning_messages(future_surplus, year_5_metrics['Operating Surplus'])  # Fixed key name

    st.divider()
    
    # Project Funding Sources section
    st.subheader(f"Project Funding Sources (Total Project Cost: ${total_cost:,.0f})")
    metric_col, chart_col = st.columns([1, 3])
    
    with metric_col:
        metrics.render_funding_metrics(
            total_assessment=total_assessment,
            assessment_per_member=assessment_per_member,
            total_bond_funding=total_bond_funding,
            bond_participants=financing_options['bond_participants'],
            remaining_to_finance=remaining_to_finance,
            total_cost=total_cost
        )
    
    with chart_col:
        funding_data = pd.DataFrame({
            'Source': ['Assessments', 'The Footnote', 'Commercial Loan'],
            'Amount': [total_assessment, total_bond_funding, remaining_to_finance]
        })
        charts.render_funding_sources_chart(funding_data)
    
    st.divider()
    
    # Time-based Projections section
    st.subheader("20-Year Financial Projections")
    
    # Generate projections for key years
    key_years = [0, 5, 10, 15, 20]
    projections = pd.DataFrame([
        calculate_year_metrics(YearMetricsInputs(
            year=year,
            future_total_revenue=future_total_revenue,
            inflation_rate=inflation_rate,
            current_expenses=config.get_operating_metric('EXPENSES'),
            annual_bond_payment=finance_metrics['annual_bond_payment'],
            annual_loan_payment=finance_metrics['annual_loan_payment'],
            bond_term=financing_options['bond_term'],
            commercial_term=financing_options['commercial_term']
        ))
        for year in key_years
    ])

    # Render projections table and chart
    charts.render_projections_table(projections)
    charts.render_trends_chart(projections)