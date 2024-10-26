"""
Input components for the Daleview Pool Financial Calculator.
Handles all user input sections and validation.
"""
import streamlit as st
from typing import Dict, Union
from .. import config

def render_current_revenue_breakdown():
    """Render the current revenue breakdown section"""
    with st.expander("Current Revenue Breakdown", expanded=False):
        current_metrics = {
            "Current Members": f"{config.get_operating_metric('MEMBERS')}",
            "Current Average Dues": f"${config.get_operating_metric('AVG_DUES'):.2f}",
            "Current Membership Revenue": f"${config.get_operating_metric('DUES_REVENUE'):,.2f}",
            "Current Swim Team Revenue": f"${config.get_operating_metric('SWIM_TEAM_REVENUE'):,.2f}",
            "Current Winter Swim Revenue": f"${config.get_operating_metric('WINTER_SWIM_REVENUE'):,.2f}",
            "Current Other Revenue": f"${config.get_operating_metric('OTHER_REVENUE'):,.2f}"
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
        member_range = config.get_input_range('MEMBERS')
        dues_range = config.get_input_range('DUES')
        
        future_members = st.slider(
            "Future Number of Members",
            min_value=member_range[0],
            max_value=member_range[1],
            value=config.get_operating_metric('MEMBERS'),
            step=5
        )
        
        future_avg_dues = st.slider(
            "Future Average Dues per Member",
            min_value=dues_range[0],
            max_value=dues_range[1],
            value=int(config.get_operating_metric('AVG_DUES')),
            step=25,
            format="$%d"
        )
    
    with st.expander("Future Non-Membership Revenue", expanded=False):
        swim_range = config.get_input_range('SWIM_TEAM')
        winter_range = config.get_input_range('WINTER_SWIM')
        other_range = config.get_input_range('OTHER')
        
        future_swim_team = st.slider(
            "Swim Team Revenue",
            min_value=swim_range[0],
            max_value=swim_range[1],
            value=config.get_operating_metric('SWIM_TEAM_REVENUE'),
            step=1000,
            format="$%d"
        )
        
        future_winter_swim = st.slider(
            "Winter Swim Revenue",
            min_value=winter_range[0],
            max_value=winter_range[1],
            value=config.get_operating_metric('WINTER_SWIM_REVENUE'),
            step=1000,
            format="$%d"
        )
        
        future_other = st.slider(
            "Other Revenue",
            min_value=other_range[0],
            max_value=other_range[1],
            value=config.get_operating_metric('OTHER_REVENUE'),
            step=1000,
            format="$%d"
        )
    
    revenue_model = {
        'members': future_members,
        'avg_dues': future_avg_dues,
        'swim_team': future_swim_team,
        'winter_swim': future_winter_swim,
        'other': future_other
    }
    
    if validate_revenue_model(revenue_model):
        return revenue_model
    return None

def validate_revenue_model(revenue_model: Dict[str, Union[int, float]]) -> bool:
    """
    Validate revenue model inputs for consistency and reasonable values.
    
    Args:
        revenue_model: Dictionary containing revenue model parameters
        
    Returns:
        True if valid, False otherwise
    """
    try:
        total_revenue = (revenue_model['members'] * revenue_model['avg_dues'] +
                        revenue_model['swim_team'] + 
                        revenue_model['winter_swim'] + 
                        revenue_model['other'])
        
        if total_revenue <= 0:
            st.error("Total revenue must be positive")
            return False
            
        if revenue_model['members'] * revenue_model['avg_dues'] < revenue_model['swim_team']:
            st.warning("Swim team revenue exceeds membership revenue - please verify")
            
        return True
        
    except KeyError as e:
        st.error(f"Missing required field: {e}")
        return False
    except Exception as e:
        st.error(f"Validation error: {e}")
        return False

def render_project_cost_section():
    """Render the project cost and assessment section"""
    with st.expander("Project Cost & Assessment", expanded=True):
        cost_range = config.get_input_range('PROJECT_COST')
        assessment_range = config.get_input_range('ASSESSMENT')
        
        total_cost = st.slider(
            "Total Project Cost",
            min_value=cost_range[0],
            max_value=cost_range[1],
            value=2_000_000,
            step=100_000,
            format="$%d"
        )
        
        assessment_per_member = st.slider(
            "One-Time Assessment per Member",
            min_value=assessment_range[0],
            max_value=assessment_range[1],
            value=2_000,
            step=100,
            format="$%d"
        )
        
        total_assessment = config.get_operating_metric('MEMBERS') * assessment_per_member
        st.info(f"Total Assessment Revenue: ${total_assessment:,.2f}")
    
    return total_cost, assessment_per_member, total_assessment

def render_financing_options(future_members: int):
    """
    Render the financing options section.
    
    Args:
        future_members: Number of future members for bond participation calculation
    """
    with st.expander("Financing Options", expanded=True):
        st.write("**The Footnote (Membership Bond Program)**")
        bond_participants = st.slider(
            "Number of Bond Participants",
            min_value=0,
            max_value=future_members,
            value=min(100, future_members),
            step=5
        )
        
        bond_range = config.get_input_range('BOND')
        avg_bond_amount = st.slider(
            "Average Bond Amount",
            min_value=bond_range[0],
            max_value=bond_range[1],
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