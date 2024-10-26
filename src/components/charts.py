"""
Chart components for the Daleview Pool Financial Calculator.
Handles all data visualization using Plotly.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict
from dataclasses import dataclass
from .. import styles

COLUMN_NAMES = {
    'YEAR': 'Year',
    'REVENUE': 'Revenue',
    'OPERATING_EXPENSES': 'Operating Expenses',
    'DEBT_SERVICE': 'Debt Service',
    'DEBT_PERCENTAGE': 'Debt % of Costs',
    'OPERATING_SURPLUS': 'Operating Surplus'  # Note the space instead of underscore
}

CHART_METRICS = {
    COLUMN_NAMES['REVENUE']: 'revenue',
    COLUMN_NAMES['OPERATING_EXPENSES']: 'expenses',
    COLUMN_NAMES['DEBT_SERVICE']: 'debt',
    COLUMN_NAMES['OPERATING_SURPLUS']: 'surplus'
}

@dataclass
class ChartDimensions:
    """Container for chart dimension calculations"""
    width: int
    height: int
    margin_top: int = 20
    margin_bottom: int = 20
    margin_left: int = 20
    margin_right: int = 20
    
    @property
    def margins(self) -> Dict[str, int]:
        """Get plotly margin dictionary"""
        return {
            't': self.margin_top,
            'b': self.margin_bottom,
            'l': self.margin_left,
            'r': self.margin_right
        }

def render_funding_sources_chart(funding_data: pd.DataFrame, container_width: Optional[int] = None) -> None:
    """
    Render funding sources pie chart with responsive sizing.
    
    Args:
        funding_data: DataFrame with Source and Amount columns
        container_width: Optional width to make chart responsive
    """
    try:
        # Validate input data
        if not isinstance(funding_data, pd.DataFrame):
            raise ValueError("funding_data must be a pandas DataFrame")
        
        required_columns = ['Source', 'Amount']
        if not all(col in funding_data.columns for col in required_columns):
            raise ValueError(f"funding_data must contain columns: {required_columns}")
        
        if funding_data['Amount'].sum() <= 0:
            raise ValueError("Total funding amount must be positive")
        
        # Calculate chart dimensions
        dims = ChartDimensions(
            width=container_width if container_width else 800,
            height=min(400, container_width * 0.6 if container_width else 400)
        )
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=funding_data['Source'],
            values=funding_data['Amount'],
            hole=.3,
            textposition='outside',
            textinfo='percent+label',
            showlegend=True,
            marker=dict(colors=styles.CHART_COLORS['funding_sources']),
            hovertemplate="%{label}<br>$%{value:,.0f}<br>%{percent}<extra></extra>"
        )])
        
        # Update layout
        fig.update_layout(
            height=dims.height,
            margin=dims.margins,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error rendering funding sources chart: {str(e)}")
        st.write("Please check your data and try again.")

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
                # Format as currency with no decimal places
                display_df[col] = display_df[col].apply(lambda x: f"${int(round(x)):,}")
        
        # Format percentage column as whole number
        if 'Debt % of Costs' in display_df.columns:
            display_df['Debt % of Costs'] = display_df['Debt % of Costs'].apply(lambda x: f"{int(round(x))}%")
        
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

def render_trends_chart(projections: pd.DataFrame) -> None:
    """
    Render the financial trends chart showing key metrics over time.
    
    Args:
        projections: DataFrame containing year-by-year projections
    """
    try:
        if not isinstance(projections, pd.DataFrame):
            raise ValueError("projections must be a pandas DataFrame")
        
        # Create figure
        fig = go.Figure()
        
        # Define metrics mapping (updated to match the actual column names)
        metrics = {
            'Revenue': 'revenue',
            'Operating Expenses': 'expenses',
            'Debt Service': 'debt',
            'Operating Surplus': 'surplus'
        }
        
        # Add traces for each metric
        for display_label, color_key in metrics.items():
            if display_label in projections.columns:
                fig.add_trace(go.Scatter(
                    x=projections['Year'].apply(lambda x: f"Year {x}"),
                    y=projections[display_label],
                    name=display_label,
                    line=dict(color=styles.CHART_COLORS['trends'][color_key]),
                    hovertemplate=f"{display_label}: ${'%{y:,.0f}'}<extra></extra>"
                ))
        
        # Update layout
        fig.update_layout(
            title='20-Year Financial Trends',
            xaxis_title='Year',
            yaxis_title='Amount ($)',
            height=400,
            showlegend=True,
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor="white",
                font_size=12
            ),
            yaxis=dict(
                tickformat="$,.0f"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error rendering trends chart: {str(e)}")
        st.write("Please check your data and try again.")

def format_currency(value: float) -> str:
    """Helper function to format currency values"""
    return f"${value:,.0f}"

def format_percentage(value: float) -> str:
    """Helper function to format percentage values"""
    return f"{value:.1f}%"