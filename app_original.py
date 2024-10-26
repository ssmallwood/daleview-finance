import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(page_title="Daleview Pool Financial Calculator", layout="wide")
st.title("Daleview Pool Renovation Financial Model")

# Custom CSS to style the expandable menu headers
st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
        background-color: #f0f2f6 !important;
        padding: 0.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Constants from current operations
CURRENT_MEMBERS = 325
CURRENT_DUES_REVENUE = 226760
CURRENT_AVG_DUES = CURRENT_DUES_REVENUE / CURRENT_MEMBERS
CURRENT_SWIM_TEAM_REVENUE = 45000
CURRENT_WINTER_SWIM_REVENUE = 71000
CURRENT_OTHER_REVENUE = 398000 - CURRENT_DUES_REVENUE - CURRENT_SWIM_TEAM_REVENUE - CURRENT_WINTER_SWIM_REVENUE
CURRENT_EXPENSES = 347000

# Calculate current total revenue at the start
CURRENT_TOTAL_REVENUE = CURRENT_DUES_REVENUE + CURRENT_SWIM_TEAM_REVENUE + CURRENT_WINTER_SWIM_REVENUE + CURRENT_OTHER_REVENUE

# Create two main columns
left_col, right_col = st.columns([1, 2])

with left_col:
    with st.expander("Current Revenue Breakdown", expanded=False):
        current_metrics = {
            "Current Members": f"{CURRENT_MEMBERS}",
            "Current Average Dues": f"${CURRENT_AVG_DUES:.2f}",
            "Current Membership Revenue": f"${CURRENT_DUES_REVENUE:,.2f}",
            "Current Swim Team Revenue": f"${CURRENT_SWIM_TEAM_REVENUE:,.2f}",
            "Current Winter Swim Revenue": f"${CURRENT_WINTER_SWIM_REVENUE:,.2f}",
            "Current Other Revenue": f"${CURRENT_OTHER_REVENUE:,.2f}"
        }
        
        for key, value in current_metrics.items():
            col1, col2 = st.columns([2, 1])
            col1.write(key)
            col2.write(value)

    with st.expander("Economic Assumptions", expanded=True):
        inflation_rate = st.slider(
            "Annual Inflation Rate",
            min_value=0.0,
            max_value=5.0,
            value=2.5,
            step=0.1,
            format="%f%%",
            help="Expected annual inflation rate"
        )

    with st.expander("Future Revenue Model", expanded=True):
        future_members = st.slider(
            "Future Number of Members",
            min_value=250,
            max_value=400,
            value=CURRENT_MEMBERS,
            step=5
        )
        
        future_avg_dues = st.slider(
            "Future Average Dues per Member",
            min_value=500,
            max_value=1500,
            value=int(CURRENT_AVG_DUES),
            step=25,
            format="$%d"
        )
    
    with st.expander("Future Non-Membership Revenue", expanded=False):
        future_swim_team = st.slider(
            "Swim Team Revenue",
            min_value=0,
            max_value=100_000,
            value=CURRENT_SWIM_TEAM_REVENUE,
            step=1000,
            format="$%d"
        )
        future_winter_swim = st.slider(
            "Winter Swim Revenue",
            min_value=0,
            max_value=200_000,
            value=CURRENT_WINTER_SWIM_REVENUE,
            step=1000,
            format="$%d"
        )
        future_other = st.slider(
            "Other Revenue",
            min_value=0,
            max_value=200_000,
            value=CURRENT_OTHER_REVENUE,
            step=1000,
            format="$%d"
        )

    with st.expander("Project Cost & Assessment", expanded=True):
        total_cost = st.slider(
            "Total Project Cost",
            min_value=1_000_000,
            max_value=3_000_000,
            value=2_000_000,
            step=100_000,
            format="$%d"
        )
        assessment_per_member = st.slider(
            "One-Time Assessment per Member",
            min_value=0,
            max_value=5_000,
            value=2_000,
            step=100,
            format="$%d"
        )
        total_assessment = CURRENT_MEMBERS * assessment_per_member
        st.info(f"Total Assessment Revenue: ${total_assessment:,.2f}")
    
    with st.expander("Financing Options", expanded=True):
        st.write("**The Footnote (Membership Bond Program)**")
        bond_participants = st.slider(
            "Number of Bond Participants",
            min_value=0,
            max_value=future_members,
            value=min(100, future_members),
            step=5
        )
        avg_bond_amount = st.slider(
            "Average Bond Amount",
            min_value=1_000,
            max_value=10_000,
            value=5_000,
            step=500,
            format="$%d"
        )
        bond_interest_rate = st.slider(
            "Bond Interest Rate",
            min_value=3.0,
            max_value=8.0,
            value=5.5,
            step=0.1,
            format="%f%%"
        )
        bond_term = st.slider(
            "Bond Term (Years)",
            min_value=5,
            max_value=15,
            value=10,
            step=1,
            format="%d years"
        )
        
        st.write("**Commercial Loan**")
        commercial_interest_rate = st.slider(
            "Commercial Loan Interest Rate",
            min_value=5.0,
            max_value=12.0,
            value=8.5,
            step=0.1,
            format="%f%%"
        )
        commercial_term = st.slider(
            "Commercial Loan Term (Years)",
            min_value=10,
            max_value=30,
            value=20,
            step=1,
            format="%d years"
        )

# Define calculate_year_metrics function before using it
def calculate_year_metrics(year):
    # Inflation factors
    inflation_factor = (1 + inflation_rate/100) ** year
    
    # Revenue with inflation
    projected_revenue = future_total_revenue * inflation_factor
    projected_expenses = CURRENT_EXPENSES * inflation_factor
    
    # Debt service (constant, doesn't change with inflation)
    year_bond_payment = annual_bond_payment if year < bond_term else 0
    year_loan_payment = annual_loan_payment if year < commercial_term else 0
    year_debt_service = year_bond_payment + year_loan_payment
    
    # Calculate metrics
    total_costs = projected_expenses + year_debt_service
    debt_service_percentage = (year_debt_service / total_costs) * 100 if total_costs > 0 else 0
    operating_surplus = projected_revenue - total_costs
    
    return {
        'Year': year,
        'Revenue': projected_revenue,
        'Operating Expenses': projected_expenses,
        'Debt Service': year_debt_service,
        'Debt % of Costs': debt_service_percentage,
        'Operating Surplus': operating_surplus
    }

with right_col:
    # Calculate all financial metrics first
    future_dues_revenue = future_members * future_avg_dues
    future_total_revenue = future_dues_revenue + future_swim_team + future_winter_swim + future_other
    
    # Calculate financing components
    total_bond_funding = bond_participants * avg_bond_amount
    remaining_to_finance = total_cost - total_bond_funding - total_assessment
    
    # Bond payment calculation
    bond_monthly_rate = bond_interest_rate / (12 * 100)
    bond_months = bond_term * 12
    if total_bond_funding > 0:
        monthly_bond_payment = total_bond_funding * (bond_monthly_rate * (1 + bond_monthly_rate)**bond_months) / ((1 + bond_monthly_rate)**bond_months - 1)
        annual_bond_payment = monthly_bond_payment * 12
        total_bond_cost = annual_bond_payment * bond_term
    else:
        monthly_bond_payment = 0
        annual_bond_payment = 0
        total_bond_cost = 0
    
    # Commercial loan calculation
    commercial_monthly_rate = commercial_interest_rate / (12 * 100)
    commercial_months = commercial_term * 12
    if remaining_to_finance > 0:
        monthly_loan_payment = remaining_to_finance * (commercial_monthly_rate * (1 + commercial_monthly_rate)**commercial_months) / ((1 + commercial_monthly_rate)**commercial_months - 1)
        annual_loan_payment = monthly_loan_payment * 12
        total_loan_cost = annual_loan_payment * commercial_term
    else:
        monthly_loan_payment = 0
        annual_loan_payment = 0
        total_loan_cost = 0
    
    total_annual_debt_service = annual_bond_payment + annual_loan_payment
    total_cost_of_borrowing = total_bond_cost + total_loan_cost - total_bond_funding - remaining_to_finance

    # Operating Financial Impact
    st.subheader("Operating Financial Impact")
    current_surplus = CURRENT_TOTAL_REVENUE - CURRENT_EXPENSES
    future_surplus = future_total_revenue - CURRENT_EXPENSES - total_annual_debt_service
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Current Operating Surplus",
            f"${current_surplus:,.0f}",
            delta=f"{(current_surplus/CURRENT_TOTAL_REVENUE*100):.1f}% of revenue"
        )
    with col2:
        st.metric(
            "Total Cost of Borrowing",
            f"${total_cost_of_borrowing:,.0f}",
            delta=f"{(total_cost_of_borrowing/total_cost*100):.1f}% of project"
        )
    with col3:
        st.metric(
            "Initial Annual Debt Service",
            f"${total_annual_debt_service:,.0f}",
            delta=f"${total_annual_debt_service/12:,.0f} monthly"
        )
    with col4:
        st.metric(
            "Future Operating Surplus",
            f"${future_surplus:,.0f}",
            delta=f"${future_surplus - current_surplus:,.0f} change"
        )

    # Warning messages with Year 5 projection
    year_5_metrics = calculate_year_metrics(5)
    year_5_surplus = year_5_metrics['Operating Surplus']
    if future_surplus < 0:
        st.error(
            f"⚠️ Warning: This scenario results in an initial deficit of ${abs(future_surplus):,.0f}\n\n" +
            f"Year 5 projection shows a {'surplus' if year_5_surplus > 0 else 'deficit'} of ${abs(year_5_surplus):,.0f}"
        )
    elif future_surplus < 10000:
        st.warning(f"⚠️ Caution: This scenario leaves a very small initial surplus of ${future_surplus:,.0f}")
    else:
        st.success(f"✅ This scenario maintains a healthy initial surplus of ${future_surplus:,.0f}")
    
    st.divider()

    # Project Funding Sources with Pie Chart
    st.subheader(f"Project Funding Sources (Total Project Cost: ${total_cost:,.0f})")
    metric_col, chart_col = st.columns([1, 3])
    
    with metric_col:
        st.metric(
            "Member Assessments",
            f"${total_assessment:,.0f}",
            delta=f"${assessment_per_member:,.0f} per member"
        )
        st.metric(
            "The Footnote",
            f"${total_bond_funding:,.0f}",
            delta=f"{bond_participants} participants"
        )
        st.metric(
            "Commercial Loan",
            f"${remaining_to_finance:,.0f}",
            delta=f"{(remaining_to_finance/total_cost*100):.1f}% of total"
        )
    
    with chart_col:
        funding_sources = {
            'Source': ['Assessments', 'The Footnote', 'Commercial Loan'],
            'Amount': [total_assessment, total_bond_funding, remaining_to_finance]
        }
        fig = go.Figure(data=[go.Pie(
            labels=funding_sources['Source'],
            values=funding_sources['Amount'],
            hole=.3,
            textposition='outside',
            textinfo='percent',
            showlegend=True,
            marker=dict(colors=['#ff9999', '#66b3ff', '#99ff99'])
        )])
        fig.update_layout(
            height=400,
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    # Time-based Projections
    st.subheader("20-Year Financial Projections")
    
    # Generate projections for key years
    key_years = [0, 5, 10, 15, 20]
    projections = pd.DataFrame([calculate_year_metrics(year) for year in key_years])
    
    # Create formatted display table
    display_df = projections.copy()
    for col in ['Revenue', 'Operating Expenses', 'Debt Service', 'Operating Surplus']:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
    display_df['Debt % of Costs'] = display_df['Debt % of Costs'].apply(lambda x: f"{x:.1f}%")
    display_df['Year'] = display_df['Year'].apply(lambda x: f"Year {x}")
    
    st.dataframe(display_df, hide_index=True, use_container_width=True)
       
    # Create trend visualization
    trend_fig = go.Figure()
    
    # Add traces for each metric
    trend_fig.add_trace(go.Scatter(
        x=projections['Year'],
        y=projections['Revenue'],
        name='Revenue',
        line=dict(color='green')
    ))
    trend_fig.add_trace(go.Scatter(
        x=projections['Year'],
        y=projections['Operating Expenses'],
        name='Operating Expenses',
        line=dict(color='red')
    ))
    trend_fig.add_trace(go.Scatter(
        x=projections['Year'],
        y=projections['Debt Service'],
        name='Debt Service',
        line=dict(color='blue')
    ))
    trend_fig.add_trace(go.Scatter(
        x=projections['Year'],
        y=projections['Operating Surplus'],
        name='Operating Surplus',
        line=dict(color='purple')
    ))
    
    trend_fig.update_layout(
        title='20-Year Financial Trends',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(trend_fig, use_container_width=True)