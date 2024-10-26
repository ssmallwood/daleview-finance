"""
Core calculation functions for the Daleview Pool Financial Calculator.
"""
from typing import Dict, Union
import pandas as pd
from dataclasses import dataclass

@dataclass
class FinancingInputs:
    """Container for financing calculation inputs"""
    total_bond_funding: float
    bond_term: int
    bond_interest_rate: float
    remaining_to_finance: float
    commercial_term: int
    commercial_interest_rate: float

@dataclass
class YearMetricsInputs:
    """Container for year metrics calculation inputs"""
    year: int
    future_total_revenue: float
    inflation_rate: float
    current_expenses: float
    annual_bond_payment: float
    annual_loan_payment: float
    bond_term: int
    commercial_term: int

def calculate_monthly_payment(principal: float, rate: float, months: int) -> float:
    """
    Calculate monthly payment for a loan.
    
    Args:
        principal: Loan principal amount
        rate: Annual interest rate as percentage
        months: Total number of months
        
    Returns:
        Monthly payment amount
    """
    if principal <= 0:
        return 0
    monthly_rate = rate / (12 * 100)
    return principal * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)

def calculate_financing_metrics(inputs: FinancingInputs) -> Dict[str, float]:
    """
    Calculate financing metrics for both bond and commercial loan components.
    
    Args:
        inputs: FinancingInputs dataclass containing all required parameters
    
    Returns:
        Dictionary containing all financing metrics
    """
    # Calculate bond payments
    bond_monthly_payment = calculate_monthly_payment(
        inputs.total_bond_funding,
        inputs.bond_interest_rate,
        inputs.bond_term * 12
    )
    annual_bond_payment = bond_monthly_payment * 12
    total_bond_cost = annual_bond_payment * inputs.bond_term
    
    # Calculate commercial loan payments
    loan_monthly_payment = calculate_monthly_payment(
        inputs.remaining_to_finance,
        inputs.commercial_interest_rate,
        inputs.commercial_term * 12
    )
    annual_loan_payment = loan_monthly_payment * 12
    total_loan_cost = annual_loan_payment * inputs.commercial_term
    
    return {
        'monthly_bond_payment': bond_monthly_payment,
        'annual_bond_payment': annual_bond_payment,
        'total_bond_cost': total_bond_cost,
        'monthly_loan_payment': loan_monthly_payment,
        'annual_loan_payment': annual_loan_payment,
        'total_loan_cost': total_loan_cost,
        'total_annual_debt_service': annual_bond_payment + annual_loan_payment,
        'total_cost_of_borrowing': (total_bond_cost + total_loan_cost - 
                                  inputs.total_bond_funding - inputs.remaining_to_finance)
    }

def get_metric_key(key: str) -> str:
    """
    Get the standardized metric key name.
    
    Args:
        key: The metric key to standardize
        
    Returns:
        Standardized key name
    """
    KEY_MAPPING = {
        'YEAR': 'Year',
        'REVENUE': 'Revenue',
        'OPERATING_EXPENSES': 'Operating Expenses',
        'DEBT_SERVICE': 'Debt Service',
        'DEBT_PERCENTAGE': 'Debt % of Costs',
        'OPERATING_SURPLUS': 'Operating Surplus'
    }
    return KEY_MAPPING.get(key, key)

def calculate_year_metrics(inputs: YearMetricsInputs) -> Dict[str, Union[int, float]]:
    """
    Calculate financial metrics for a specific year.
    
    Args:
        inputs: YearMetricsInputs dataclass containing all required parameters
    
    Returns:
        Dictionary containing calculated metrics for the specified year
    """
    inflation_factor = (1 + inputs.inflation_rate/100) ** inputs.year
    
    projected_revenue = inputs.future_total_revenue * inflation_factor
    projected_expenses = inputs.current_expenses * inflation_factor
    
    year_bond_payment = inputs.annual_bond_payment if inputs.year < inputs.bond_term else 0
    year_loan_payment = inputs.annual_loan_payment if inputs.year < inputs.commercial_term else 0
    year_debt_service = year_bond_payment + year_loan_payment
    
    total_costs = projected_expenses + year_debt_service
    debt_service_percentage = (year_debt_service / total_costs * 100) if total_costs > 0 else 0
    operating_surplus = projected_revenue - total_costs
    
    # Update: Consistent column names for the DataFrame
    return {
        'Year': inputs.year,
        'Revenue': projected_revenue,
        'Operating Expenses': projected_expenses,
        'Debt Service': year_debt_service,
        'Debt % of Costs': debt_service_percentage,
        'Operating Surplus': operating_surplus
    }