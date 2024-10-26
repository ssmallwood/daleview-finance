import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from .. import styles

def render_funding_sources_chart(funding_data):
    """Render the funding sources pie chart"""
    fig = go.Figure(data=[go.Pie(
        labels=funding_data['Source'],
        values=funding_data['Amount'],
        hole=.3,
        textposition='outside',
        textinfo='percent',
        showlegend=True,
        marker=dict(colors=styles.CHART_COLORS['funding_sources'])
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

def render_projections_table(projections):
    """Render the financial projections table"""
    display_df = projections.copy()
    
    # Format the columns
    for col in ['Revenue', 'Operating Expenses', 'Debt Service', 'Operating Surplus']:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
    display_df['Debt % of Costs'] = display_df['Debt % of Costs'].apply(lambda x: f"{x:.1f}%")
    display_df['Year'] = display_df['Year'].apply(lambda x: f"Year {x}")
    
    st.dataframe(display_df, hide_index=True, use_container_width=True)

def render_trends_chart(projections):
    """Render the financial trends chart"""
    fig = go.Figure()
    
    # Add traces for each metric
    metrics = {
        'Revenue': 'revenue',
        'Operating Expenses': 'expenses',
        'Debt Service': 'debt',
        'Operating Surplus': 'surplus'
    }
    
    for label, metric in metrics.items():
        fig.add_trace(go.Scatter(
            x=projections['Year'],
            y=projections[label],
            name=label,
            line=dict(color=styles.CHART_COLORS['trends'][metric])
        ))
    
    fig.update_layout(
        title='20-Year Financial Trends',
        xaxis_title='Year',
        yaxis_title='Amount ($)',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)