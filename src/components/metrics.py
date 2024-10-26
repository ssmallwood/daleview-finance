import streamlit as st
from .. import config

def render_financial_impact_metrics(current_surplus, total_cost_of_borrowing, 
                                  total_annual_debt_service, future_surplus, total_cost):
    """Render the financial impact metrics section"""
    st.subheader("Operating Financial Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Current Operating Surplus",
            f"${current_surplus:,.0f}",
            delta=f"{(current_surplus/config.CURRENT_TOTAL_REVENUE*100):.1f}% of revenue"
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

def render_warning_messages(future_surplus, year_5_surplus):
    """Render warning messages based on financial projections"""
    if future_surplus < 0:
        st.error(
            f"⚠️ Warning: This scenario results in an initial deficit of ${abs(future_surplus):,.0f}\n\n" +
            f"Year 5 projection shows a {'surplus' if year_5_surplus > 0 else 'deficit'} of ${abs(year_5_surplus):,.0f}"
        )
    elif future_surplus < 10000:
        st.warning(f"⚠️ Caution: This scenario leaves a very small initial surplus of ${future_surplus:,.0f}")
    else:
        st.success(f"✅ This scenario maintains a healthy initial surplus of ${future_surplus:,.0f}")

def render_funding_metrics(total_assessment, assessment_per_member, 
                         total_bond_funding, bond_participants,
                         remaining_to_finance, total_cost):
    """Render the funding source metrics"""
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