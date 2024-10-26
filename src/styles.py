# CSS styles for the application
STYLES = """
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
"""

# Color schemes for charts
CHART_COLORS = {
    'funding_sources': ['#ff9999', '#66b3ff', '#99ff99'],
    'trends': {
        'revenue': 'green',
        'expenses': 'red',
        'debt': 'blue',
        'surplus': 'purple'
    }
}