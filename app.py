import streamlit as st
import pandas as pd
from src import config, calculations, styles
from src.components import inputs, metrics, charts

# Page configuration
st.set_page_config(page_title="Daleview Pool Financial Calculator", layout="wide")
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
    future_total_revenue = (
        revenue_model['members'] * revenue_model['avg_dues'] +
        revenue_model['swim_team'] + 
        revenue_model['winter_swim'] + 
        revenue_model['other']
    )
    
    total_cost, assessment_per_member, total_assessment = inputs.render_project_cost_section()
    
    financing_options = inputs.render_financing_options(revenue_model['members'])

# Calculate financing metrics
total_bond_funding = financing_options['bond_participants'] * financing_options['avg_bond_amount']
remaining_to_finance = total_cost - total_bond_funding - total_assessment

finance_metrics = calculations.calculate_financing_metrics(
    total_bond_funding=total_bond_funding,
    bond_term=financing_options['bond_term'],
    bond_interest_rate=financing_options['bond_interest_rate'],
    remaining_to_finance=remaining_to_finance,
    commercial_term=financing_options['commercial_term'],
    commercial_interest_rate=financing_options['commercial_interest_rate']
)

# Right column - Results and visualizations
with right_col:
    # Calculate key metrics
    current_surplus = config.CURRENT_TOTAL_REVENUE - config.CURRENT_EXPENSES
    future_surplus = future_total_revenue - config.CURRENT_EXPENSES - finance_metrics['total_annual_debt_service']
    
    # Render financial impact section
    metrics.render_financial_impact_metrics(
        current_surplus=current_surplus,
        total_cost_of_borrowing=finance_metrics['total_cost_of_borrowing'],
        total_annual_debt_service=finance_metrics['total_annual_debt_service'],
        future_surplus=future_surplus,
        total_cost=total_cost
    )
    
    # Calculate and render 5-year projection warning
    year_5_metrics = calculations.calculate_year_metrics(
        year=5,
        future_total_revenue=future_total_revenue,
        inflation_rate=inflation_rate,
        current_expenses=config.CURRENT_EXPENSES,
        annual_bond_payment=finance_metrics['annual_bond_payment'],
        annual_loan_payment=finance_metrics['annual_loan_payment'],
        bond_term=financing_options['bond_term'],
        commercial_term=financing_options['commercial_term']
    )
    metrics.render_warning_messages(future_surplus, year_5_metrics['Operating Surplus'])
    
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
        funding_data = {
            'Source': ['Assessments', 'The Footnote', 'Commercial Loan'],
            'Amount': [total_assessment, total_bond_funding, remaining_to_finance]
        }
        charts.render_funding_sources_chart(funding_data)
    
    st.divider()
    
    # Time-based Projections section
    st.subheader("20-Year Financial Projections")
    
    # Generate projections for key years
    key_years = [0, 5, 10, 15, 20]
    projections = pd.DataFrame([
        calculations.calculate_year_metrics(
            year=year,
            future_total_revenue=future_total_revenue,
            inflation_rate=inflation_rate,
            current_expenses=config.CURRENT_EXPENSES,
            annual_bond_payment=finance_metrics['annual_bond_payment'],
            annual_loan_payment=finance_metrics['annual_loan_payment'],
            bond_term=financing_options['bond_term'],
            commercial_term=financing_options['commercial_term']
        )
        for year in key_years
    ])
    
    # Render projections table and chart
    charts.render_projections_table(projections)
    charts.render_trends_chart(projections)