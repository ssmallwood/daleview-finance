"""
Metrics components for the Daleview Pool Financial Calculator.
Handles display of financial metrics and warning messages.
"""
import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import Optional

@dataclass
class FinancialMetrics:
    """Container for key financial metrics"""
    current_surplus: float
    future_surplus: float
    total_cost: float
    total_cost_of_borrowing: float
    total_annual_debt_service: float
    
    @property
    def surplus_change(self) -> float:
        """Calculate change in surplus"""
        return self.future_surplus - self.current_surplus
    
    @property
    def debt_service_ratio(self) -> float:
        """Calculate debt service as percentage of total cost"""
        return (self.total_annual_debt_service / self.total_cost * 100) if self.total_cost > 0 else 0
    
    @property
    def borrowing_ratio(self) -> float:
        """Calculate total cost of borrowing as percentage of project cost"""
        return (self.total_cost_of_borrowing / self.total_cost * 100) if self.total_cost > 0 else 0

def render_financial_impact_metrics(
    current_surplus: float,
    total_cost_of_borrowing: float,
    total_annual_debt_service: float,
    future_surplus: float,
    total_cost: float
) -> None:
    """
    Render the financial impact metrics section.
    
    Args:
        current_surplus: Current operating surplus
        total_cost_of_borrowing: Total cost of all financing
        total_annual_debt_service: Annual debt service payments
        future_surplus: Projected future operating surplus
        total_cost: Total project cost
    """
    metrics = FinancialMetrics(
        current_surplus=current_surplus,
        future_surplus=future_surplus,
        total_cost=total_cost,
        total_cost_of_borrowing=total_cost_of_borrowing,
        total_annual_debt_service=total_annual_debt_service
    )
    
    st.subheader("Operating Financial Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Operating Surplus",
            f"${metrics.current_surplus:,.0f}",
            help="Current annual operating surplus before renovation"
        )
    
    with col2:
        st.metric(
            "Total Cost of Borrowing",
            f"${metrics.total_cost_of_borrowing:,.0f}",
            delta=f"{metrics.borrowing_ratio:.1f}% of project",
            help="Total interest and financing costs over the life of all loans"
        )
    
    with col3:
        st.metric(
            "Annual Debt Service",
            f"${metrics.total_annual_debt_service:,.0f}",
            delta=f"${metrics.total_annual_debt_service/12:,.0f} monthly",
            help="Total annual payments for all financing"
        )
    
    with col4:
        st.metric(
            "Future Operating Surplus",
            f"${metrics.future_surplus:,.0f}",
            delta=f"${metrics.surplus_change:,.0f} change",
            help="Projected annual operating surplus after renovation"
        )

def render_projections_table(projections: pd.DataFrame) -> None:
    """
    Render the financial projections table with formatted values.
    
    Args:
        projections: DataFrame containing year-by-year projections
    """
    try:
        if not isinstance(projections, pd.DataFrame):
            raise ValueError("projections must be a pandas DataFrame")
        
        display_df = projections.copy()
        
        # Format currency columns with consistent names
        currency_columns = ['Revenue', 'Operating Expenses', 'Debt Service', 'Operating Surplus']
        for col in currency_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
        
        # Format percentage column
        if 'Debt % of Costs' in display_df.columns:
            display_df['Debt % of Costs'] = display_df['Debt % of Costs'].apply(lambda x: f"{x:.1f}%")
        
        # Format year column
        if 'Year' in display_df.columns:
            display_df['Year'] = display_df['Year'].apply(lambda x: f"Year {x}")
        
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error rendering projections table: {str(e)}")
        st.write("Please check your data and try again.")

def render_warning_messages(future_surplus: float, year_5_surplus: float) -> None:
    """
    Render warning messages based on financial projections.
    
    Args:
        future_surplus: Initial projected operating surplus
        year_5_surplus: Projected operating surplus in year 5
    """
    def get_warning_color(surplus: float) -> str:
        """Determine warning color based on surplus amount"""
        if surplus < 0:
            return "error"
        elif surplus < 10000:
            return "warning"
        return "success"
    
    def format_message(initial_surplus: float, future_surplus: float) -> str:
        """Format warning message based on surplus values"""
        state = "deficit" if initial_surplus < 0 else "surplus"
        future_state = "deficit" if future_surplus < 0 else "surplus"
        
        msg = (f"This scenario results in an initial {state} of ${abs(initial_surplus):,.0f}\n\n"
               f"Year 5 projection shows a {future_state} of ${abs(future_surplus):,.0f}")
        
        if initial_surplus > 0 and initial_surplus < 10000:
            msg = f"Caution: This scenario leaves a very small initial surplus of ${initial_surplus:,.0f}"
        elif initial_surplus >= 10000:
            msg = f"This scenario maintains a healthy initial surplus of ${initial_surplus:,.0f}"
        
        return msg
    
    warning_type = get_warning_color(future_surplus)
    message = format_message(future_surplus, year_5_surplus)
    
    if warning_type == "error":
        st.error(f"⚠️ Warning: {message}")
    elif warning_type == "warning":
        st.warning(f"⚠️ {message}")
    else:
        st.success(f"✅ {message}")

def render_funding_metrics(
    total_assessment: float,
    assessment_per_member: float,
    total_bond_funding: float,
    bond_participants: int,
    remaining_to_finance: float,
    total_cost: float
) -> None:
    """
    Render the funding source metrics.
    
    Args:
        total_assessment: Total funding from member assessments
        assessment_per_member: Assessment amount per member
        total_bond_funding: Total funding from bonds
        bond_participants: Number of bond participants
        remaining_to_finance: Amount to be financed through commercial loan
        total_cost: Total project cost
    """
    try:
        # Calculate percentages
        assessment_percent = (total_assessment / total_cost * 100) if total_cost > 0 else 0
        bond_percent = (total_bond_funding / total_cost * 100) if total_cost > 0 else 0
        loan_percent = (remaining_to_finance / total_cost * 100) if total_cost > 0 else 0
        
        st.metric(
            "Member Assessments",
            f"${total_assessment:,.0f}",
            delta=f"${assessment_per_member:,.0f} per member",
            help=f"Represents {assessment_percent:.1f}% of total project cost"
        )
        
        st.metric(
            "The Footnote",
            f"${total_bond_funding:,.0f}",
            delta=f"{bond_participants} participants",
            help=f"Represents {bond_percent:.1f}% of total project cost"
        )
        
        st.metric(
            "Commercial Loan",
            f"${remaining_to_finance:,.0f}",
            delta=f"{loan_percent:.1f}% of total",
            help="Amount to be financed through commercial loan"
        )
    
    except Exception as e:
        st.error(f"Error calculating funding metrics: {str(e)}")
        st.write("Please check your input values and try again.")