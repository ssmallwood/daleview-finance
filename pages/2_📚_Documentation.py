import streamlit as st

st.set_page_config(page_title="Daleview Pool Calculator Documentation", layout="wide")

st.title("Documentation & Help")

with st.expander("Overview", expanded=True):
    st.markdown("""
        ## About This Calculator
        The Daleview Pool Financial Calculator helps model and visualize the financial implications 
        of the pool renovation project. It allows exploration of different scenarios for:
        - Membership levels and dues
        - Project costs and assessments
        - Financing options including bonds and commercial loans
        - Long-term financial sustainability
    """)

with st.expander("Key Financial Components"):
    st.markdown("""
        ## Current Revenue Model
        - **Membership Dues**: Primary revenue source based on member count and average dues
        - **Swim Team**: Seasonal program revenue
        - **Winter Swim**: Off-season program revenue
        - **Other Revenue**: Additional income sources
        
        ## Project Funding Sources
        1. **Member Assessments**: One-time payment from each member
        2. **The Footnote (Bond Program)**: Optional member bonds with interest
        3. **Commercial Loan**: Traditional financing for remaining costs
        
        ## Operating Costs
        - Base operating expenses adjusted for inflation
        - New debt service payments
        - Maintenance reserves
    """)

with st.expander("Using the Calculator"):
    st.markdown("""
        ## Step-by-Step Guide
        
        ### 1. Economic Assumptions
        - Set expected inflation rate
        - Impacts long-term projections
        
        ### 2. Future Revenue Model
        - Adjust membership numbers
        - Set future dues levels
        - Modify program revenue expectations
        
        ### 3. Project Cost & Assessment
        - Enter total project cost
        - Set one-time member assessment amount
        
        ### 4. Financing Options
        #### The Footnote (Membership Bond Program)
        - Number of participating members
        - Average bond amount
        - Interest rate and term
        
        #### Commercial Loan
        - Interest rate
        - Loan term
        
        ### 5. Reviewing Results
        - Operating Financial Impact
        - Project Funding Sources
        - 20-Year Financial Projections
    """)

with st.expander("Understanding the Results"):
    st.markdown("""
        ## Key Metrics Explained
        
        ### Operating Financial Impact
        - **Current Operating Surplus**: Baseline before renovation
        - **Total Cost of Borrowing**: All interest and financing costs
        - **Annual Debt Service**: Yearly loan and bond payments
        - **Future Operating Surplus**: Projected post-renovation surplus
        
        ### Project Funding Sources
        Shows breakdown between:
        - Member assessments
        - Bond program
        - Commercial loan
        
        ### 20-Year Projections
        - **Revenue**: All income sources with inflation
        - **Operating Expenses**: Base costs plus inflation
        - **Debt Service**: Annual financing payments
        - **Operating Surplus**: Net position each year
    """)

with st.expander("Limitations and Assumptions"):
    st.markdown("""
        ## Model Limitations
        
        ### Fixed Assumptions
        - Constant inflation rate
        - Stable membership levels
        - Fixed interest rates
        
        ### Simplifications
        - Linear revenue growth
        - Uniform expense inflation
        - No major unexpected costs
        
        ### Not Included
        - Market condition changes
        - Competition effects
        - Major maintenance events
        
        ## Data Sources
        - Current operating metrics from pool records
        - Industry standard financial assumptions
        - Local market analysis
    """)

with st.expander("Tips and Best Practices"):
    st.markdown("""
        ## Using the Calculator Effectively
        
        ### Start Conservative
        - Use realistic membership numbers
        - Include buffer in cost estimates
        - Consider higher interest rates
        
        ### Test Multiple Scenarios
        - Optimistic case
        - Expected case
        - Conservative case
        
        ### Watch Key Indicators
        - Operating surplus should remain positive
        - Debt service ratio below 35%
        - Maintain emergency reserves
        
        ### Common Pitfalls
        - Overestimating revenue growth
        - Underestimating inflation impact
        - Insufficient contingency
    """)