import streamlit as st
import pandas as pd
from src import config, styles
from src.calculations import FinancingInputs, YearMetricsInputs, calculate_financing_metrics, calculate_year_metrics
from src.components import inputs, metrics, charts

def main():
    # Only show the app content after successful authentication
    st.title("Daleview Pool Renovation Financial Model")

    # Add welcome message after password check but before main content
    if 'welcomed' not in st.session_state:
        with st.expander("👋 Welcome! Click here to learn how to use the calculator", expanded=True):
            st.markdown("""
                ### How This Calculator Works
                
                This tool helps explore different financial scenarios for the pool renovation project.
                Follow these steps to model your scenario:
            """)
            
            # Create three columns for our steps
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                    #### 1️⃣ Set Your Inputs
                    - Project cost
                    - Member assessment
                    - Bond participation
                    - Loan terms
                """)
                
            with col2:
                st.markdown("""
                    #### 2️⃣ Review Impact
                    - Total funding mix
                    - Annual debt payments
                    - Operating costs
                """)
                
            with col3:
                st.markdown("""
                    #### 3️⃣ Check Results
                    - Operating surplus
                    - 20-year outlook
                    - Financial health
                """)
                
            st.markdown("---")
            st.markdown("""
                💡 **Tip**: Start with the Project Cost & Assessment section on the left, 
                then explore financing options to see their impact on the right.
                
                *Need more help? Check the Documentation page in the navigation menu.*
            """)
            
            if st.button("Got it! Don't show this again"):
                st.session_state.welcomed = True
                st.rerun()

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

# Page config
st.set_page_config(
    page_title="Daleview Pool Financial Calculator",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Show navigation tip on first load and permanent reminder
if 'shown_sidebar_tip' not in st.session_state:
    st.sidebar.markdown("""
        <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
        💡 <b>Tip:</b> Click the arrow at the top left to hide this menu and get more screen space!
        </div>
    """, unsafe_allow_html=True)
    st.session_state.shown_sidebar_tip = True

# Add the permanent reminder
st.sidebar.markdown("---")
st.sidebar.markdown("↑ _Click arrow to hide menu_")

# Define pages
main_page = st.Page(main, title="Calculator", icon="💰", default=True)
docs_page = st.Page("documentation.py", title="Documentation", icon="📚")

# Set up navigation
pg = st.navigation([main_page, docs_page])

pg.run()

