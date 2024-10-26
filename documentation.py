import streamlit as st

st.title("Documentation & Help")

with st.expander("Overview", expanded=True):
    st.markdown("""
        ## About This Calculator
        The Daleview Pool Financial Calculator helps model and visualize the financial implications 
        of the pool renovation project. It provides interactive tools for exploring:
        - Membership levels and dues structures
        - Multiple revenue stream projections
        - Project costs and assessment options
        - Flexible financing combinations
        - Long-term financial sustainability metrics
        
        ### Core Features
        - **Interactive Financial Modeling**: Real-time scenario testing
        - **Comprehensive Visualizations**: Charts and projections
        - **Economic Analysis**: Inflation-adjusted forecasting
        - **Multiple Financing Options**: Combined funding sources
    """)

with st.expander("Detailed Calculation Methodologies"):
    st.markdown("""
        ## How Calculations Work

        ### 1. Revenue Calculations
        ```python
        # Base membership revenue
        future_dues_revenue = future_members * future_avg_dues

        # Total revenue including all streams
        future_total_revenue = (future_dues_revenue + 
                              future_swim_team + 
                              future_winter_swim + 
                              future_other)
        ```
        
        ### 2. Financing Calculations
        
        #### Member Assessments
        ```python
        total_assessment = current_members * assessment_per_member
        ```
        
        #### Bond Program (The Footnote)
        ```python
        total_bond_funding = bond_participants * avg_bond_amount
        monthly_rate = bond_interest_rate / (12 * 100)
        n_payments = bond_term * 12
        
        monthly_bond_payment = (total_bond_funding * 
                              (monthly_rate * (1 + monthly_rate)**n_payments) / 
                              ((1 + monthly_rate)**n_payments - 1))
        ```
        
        #### Commercial Loan
        ```python
        remaining_to_finance = total_cost - total_bond_funding - total_assessment
        monthly_rate = commercial_interest_rate / (12 * 100)
        n_payments = commercial_term * 12
        
        monthly_loan_payment = (remaining_to_finance * 
                              (monthly_rate * (1 + monthly_rate)**n_payments) / 
                              ((1 + monthly_rate)**n_payments - 1))
        ```
        
        ### 3. Time-Based Projections
        ```python
        # Inflation adjustments
        inflation_factor = (1 + inflation_rate/100) ** year
        projected_revenue = future_total_revenue * inflation_factor
        projected_expenses = current_expenses * inflation_factor
        
        # Year-specific calculations
        year_bond_payment = annual_bond_payment if year < bond_term else 0
        year_loan_payment = annual_loan_payment if year < commercial_term else 0
        year_debt_service = year_bond_payment + year_loan_payment
        
        # Financial health metrics
        total_costs = projected_expenses + year_debt_service
        debt_service_percentage = (year_debt_service / total_costs) * 100
        operating_surplus = projected_revenue - total_costs
        ```
    """)

with st.expander("Current Operating Assumptions"):
    st.markdown("""
        ## Base Operating Metrics
        
        ### Current Revenue Model
        - **Members**: 325
        - **Annual Dues Revenue**: $226,760
        - **Swim Team Revenue**: $45,000
        - **Winter Swim Revenue**: $71,000
        - **Operating Expenses**: $347,000
        
        ### Financing Parameters
        
        #### The Footnote (Membership Bond Program)
        - Term: 5-15 years (default 10)
        - Interest rates: 3-8% (default 5.5%)
        - Individual bond amounts: $1,000-$10,000
        
        #### Commercial Loan
        - Term: 10-30 years (default 20)
        - Interest rates: 5-12% (default 8.5%)
    """)

with st.expander("Using the Calculator"):
    st.markdown("""
        ## Step-by-Step Guide
        
        ### 1. Economic Assumptions
        - Set expected inflation rate for long-term projections
        - Default is 2.5%, adjustable from 0-5%
        
        ### 2. Future Revenue Model
        - **Membership Settings**
            - Adjust member count (250-400 range)
            - Set average dues ($500-$1,500 range)
        - **Additional Revenue**
            - Swim team revenue (up to $100,000)
            - Winter swim revenue (up to $200,000)
            - Other revenue sources (up to $200,000)
        
        ### 3. Project Cost & Assessment
        - Set total project cost ($1M-$3M range)
        - Configure one-time member assessment (up to $5,000)
        
        ### 4. Financing Options
        - **The Footnote Program**
            - Set number of participating members
            - Configure bond amounts and terms
        - **Commercial Loan**
            - Adjust interest rate and term
            - Calculator automatically determines required amount
        
        ### 5. Review Results
        - Check operating financial impact
        - Review funding source breakdown
        - Analyze 20-year projections
        - Evaluate warning messages
    """)

with st.expander("Understanding Results"):
    st.markdown("""
        ## Key Financial Indicators
        
        ### 1. Operating Financial Impact
        - **Current Operating Surplus**: Pre-renovation baseline
        - **Total Cost of Borrowing**: All financing costs
        - **Annual Debt Service**: Combined yearly payments
        - **Future Operating Surplus**: Post-renovation projection
        
        ### 2. Project Funding Mix
        Visualizes the proportion from each source:
        - Member assessments (upfront payments)
        - The Footnote (bond program)
        - Commercial loan (remaining amount)
        
        ### 3. Long-term Sustainability
        20-year projections showing:
        - Revenue growth with inflation
        - Operating expense trends
        - Debt service burden
        - Operating surplus/deficit patterns
        
        ### 4. Warning Messages
        Automatic alerts for:
        - Negative operating surplus
        - Low surplus margins
        - High debt service ratios
    """)

with st.expander("Limitations and Assumptions"):
    st.markdown("""
        ## Model Constraints
        
        ### Fixed Assumptions
        - Constant inflation rate throughout projection period
        - Fixed interest rates on all debt
        - Stable membership levels within scenarios
        
        ### Simplifications
        - Linear revenue growth with inflation
        - Uniform inflation across all expense categories
        - No variable rate financing options
        
        ### Not Included
        - Market condition changes
        - Competition effects
        - Major maintenance events
        - Construction period modeling
        - Seasonal revenue variations
        - Refinancing scenarios
        
        ### Conservative Approach
        The model is intentionally conservative in its estimates and designed to:
        - Highlight potential financial stress points
        - Encourage adequate financial cushions
        - Support sustainable long-term planning
    """)

with st.expander("Troubleshooting"):
    st.markdown("""
        ## Common Issues
        
        ### Invalid Scenarios
        - **Negative Operating Surplus**: Reduce debt or increase revenue
        - **High Debt Service Ratio**: Consider more member funding
        - **Low Member Participation**: Adjust bond terms or assessment
        
        ### Data Validation
        The calculator enforces:
        - Reasonable ranges for all inputs
        - Consistent relationship checks
        - Maximum financing limits
        
        ### Technical Problems
        If you encounter issues:
        1. Refresh the page
        2. Clear browser cache
        3. Check input values are within allowed ranges
        4. Verify total funding sources match project cost
    """)