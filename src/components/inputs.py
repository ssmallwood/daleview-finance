import streamlit as st
from .. import config

def render_current_revenue_breakdown():
    """Render the current revenue breakdown section"""
    with st.expander("Current Revenue Breakdown", expanded=False):
        current_metrics = {
            "Current Members": f"{config.CURRENT_MEMBERS}",
            "Current Average Dues": f"${config.CURRENT_AVG_DUES:.2f}",
            "Current Membership Revenue": f"${config.CURRENT_DUES_REVENUE:,.2f}",
            "Current Swim Team Revenue": f"${config.CURRENT_SWIM_TEAM_REVENUE:,.2f}",
            "Current Winter Swim Revenue": f"${config.CURRENT_WINTER_SWIM_REVENUE:,.2f}",
            "Current Other Revenue": f"${config.CURRENT_OTHER_REVENUE:,.2f}"
        }
        
        for key, value in current_metrics.items():
            col1, col2 = st.columns([2, 1])
            col1.write(key)
            col2.write(value)

def render_economic_assumptions():
    """Render the economic assumptions section"""
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
    return inflation_rate

def render_future_revenue_model():
    """Render the future revenue model section"""
    with st.expander("Future Revenue Model", expanded=True):
        future_members = st.slider(
            "Future Number of Members",
            min_value=config.MEMBER_RANGE[0],
            max_value=config.MEMBER_RANGE[1],
            value=config.CURRENT_MEMBERS,
            step=5
        )
        
        future_avg_dues = st.slider(
            "Future Average Dues per Member",
            min_value=config.DUES_RANGE[0],
            max_value=config.DUES_RANGE[1],
            value=int(config.CURRENT_AVG_DUES),
            step=25,
            format="$%d"
        )
    
    with st.expander("Future Non-Membership Revenue", expanded=False):
        future_swim_team = st.slider(
            "Swim Team Revenue",
            min_value=config.SWIM_TEAM_RANGE[0],
            max_value=config.SWIM_TEAM_RANGE[1],
            value=config.CURRENT_SWIM_TEAM_REVENUE,
            step=1000,
            format="$%d"
        )
        future_winter_swim = st.slider(
            "Winter Swim Revenue",
            min_value=config.WINTER_SWIM_RANGE[0],
            max_value=config.WINTER_SWIM_RANGE[1],
            value=config.CURRENT_WINTER_SWIM_REVENUE,
            step=1000,
            format="$%d"
        )
        future_other = st.slider(
            "Other Revenue",
            min_value=config.OTHER_REVENUE_RANGE[0],
            max_value=config.OTHER_REVENUE_RANGE[1],
            value=config.CURRENT_OTHER_REVENUE,
            step=1000,
            format="$%d"
        )
    
    return {
        'members': future_members,
        'avg_dues': future_avg_dues,
        'swim_team': future_swim_team,
        'winter_swim': future_winter_swim,
        'other': future_other
    }

def render_project_cost_section():
    """Render the project cost and assessment section"""
    with st.expander("Project Cost & Assessment", expanded=True):
        total_cost = st.slider(
            "Total Project Cost",
            min_value=config.PROJECT_COST_RANGE[0],
            max_value=config.PROJECT_COST_RANGE[1],
            value=2_000_000,
            step=100_000,
            format="$%d"
        )
        assessment_per_member = st.slider(
            "One-Time Assessment per Member",
            min_value=config.ASSESSMENT_RANGE[0],
            max_value=config.ASSESSMENT_RANGE[1],
            value=2_000,
            step=100,
            format="$%d"
        )
        total_assessment = config.CURRENT_MEMBERS * assessment_per_member
        st.info(f"Total Assessment Revenue: ${total_assessment:,.2f}")
    
    return total_cost, assessment_per_member, total_assessment

def render_financing_options(future_members):
    """Render the financing options section"""
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
            min_value=config.BOND_AMOUNT_RANGE[0],
            max_value=config.BOND_AMOUNT_RANGE[1],
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
    
    return {
        'bond_participants': bond_participants,
        'avg_bond_amount': avg_bond_amount,
        'bond_interest_rate': bond_interest_rate,
        'bond_term': bond_term,
        'commercial_interest_rate': commercial_interest_rate,
        'commercial_term': commercial_term
    }