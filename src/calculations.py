def calculate_financing_metrics(total_bond_funding, bond_term, bond_interest_rate,
                              remaining_to_finance, commercial_term, commercial_interest_rate):
    """Calculate all financing-related metrics"""
    # Bond payment calculation
    bond_monthly_rate = bond_interest_rate / (12 * 100)
    bond_months = bond_term * 12
    
    if total_bond_funding > 0:
        monthly_bond_payment = total_bond_funding * (
            bond_monthly_rate * (1 + bond_monthly_rate)**bond_months
        ) / ((1 + bond_monthly_rate)**bond_months - 1)
        annual_bond_payment = monthly_bond_payment * 12
        total_bond_cost = annual_bond_payment * bond_term
    else:
        monthly_bond_payment = annual_bond_payment = total_bond_cost = 0
    
    # Commercial loan calculation
    commercial_monthly_rate = commercial_interest_rate / (12 * 100)
    commercial_months = commercial_term * 12
    
    if remaining_to_finance > 0:
        monthly_loan_payment = remaining_to_finance * (
            commercial_monthly_rate * (1 + commercial_monthly_rate)**commercial_months
        ) / ((1 + commercial_monthly_rate)**commercial_months - 1)
        annual_loan_payment = monthly_loan_payment * 12
        total_loan_cost = annual_loan_payment * commercial_term
    else:
        monthly_loan_payment = annual_loan_payment = total_loan_cost = 0
    
    total_annual_debt_service = annual_bond_payment + annual_loan_payment
    total_cost_of_borrowing = (total_bond_cost + total_loan_cost - 
                              total_bond_funding - remaining_to_finance)
    
    return {
        'monthly_bond_payment': monthly_bond_payment,
        'annual_bond_payment': annual_bond_payment,
        'total_bond_cost': total_bond_cost,
        'monthly_loan_payment': monthly_loan_payment,
        'annual_loan_payment': annual_loan_payment,
        'total_loan_cost': total_loan_cost,
        'total_annual_debt_service': total_annual_debt_service,
        'total_cost_of_borrowing': total_cost_of_borrowing
    }

def calculate_year_metrics(year, future_total_revenue, inflation_rate, current_expenses,
                          annual_bond_payment, annual_loan_payment, bond_term, commercial_term):
    """Calculate financial metrics for a specific year"""
    inflation_factor = (1 + inflation_rate/100) ** year
    
    projected_revenue = future_total_revenue * inflation_factor
    projected_expenses = current_expenses * inflation_factor
    
    year_bond_payment = annual_bond_payment if year < bond_term else 0
    year_loan_payment = annual_loan_payment if year < commercial_term else 0
    year_debt_service = year_bond_payment + year_loan_payment
    
    total_costs = projected_expenses + year_debt_service
    debt_service_percentage = (year_debt_service / total_costs * 100) if total_costs > 0 else 0
    operating_surplus = projected_revenue - total_costs
    
    return {
        'Year': year,
        'Revenue': projected_revenue,
        'Operating Expenses': projected_expenses,
        'Debt Service': year_debt_service,
        'Debt % of Costs': debt_service_percentage,
        'Operating Surplus': operating_surplus
    }