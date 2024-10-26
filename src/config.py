"""
Configuration constants for the Daleview Pool Financial Calculator.
Includes current operating metrics and valid ranges for user inputs.
"""
from typing import Dict, Union, Tuple

# Operating metrics
OPERATING_METRICS = {
    'MEMBERS': 325,
    'DUES_REVENUE': 226760,
    'SWIM_TEAM_REVENUE': 45000,
    'WINTER_SWIM_REVENUE': 71000,
    'EXPENSES': 347000
}

# Calculate derived metrics
OPERATING_METRICS['AVG_DUES'] = OPERATING_METRICS['DUES_REVENUE'] / OPERATING_METRICS['MEMBERS']
OPERATING_METRICS['OTHER_REVENUE'] = (398000 - OPERATING_METRICS['DUES_REVENUE'] 
                                    - OPERATING_METRICS['SWIM_TEAM_REVENUE']
                                    - OPERATING_METRICS['WINTER_SWIM_REVENUE'])
OPERATING_METRICS['TOTAL_REVENUE'] = (OPERATING_METRICS['DUES_REVENUE']
                                    + OPERATING_METRICS['SWIM_TEAM_REVENUE']
                                    + OPERATING_METRICS['WINTER_SWIM_REVENUE']
                                    + OPERATING_METRICS['OTHER_REVENUE'])

# Input ranges with descriptive names
INPUT_RANGES = {
    'MEMBERS': (250, 400),
    'DUES': (500, 1500),
    'SWIM_TEAM': (0, 100_000),
    'WINTER_SWIM': (0, 200_000),
    'OTHER': (0, 200_000),
    'PROJECT_COST': (1_000_000, 3_000_000),
    'ASSESSMENT': (0, 5_000),
    'BOND': (1_000, 10_000)
}

def get_operating_metric(key: str) -> Union[int, float]:
    """
    Safely retrieve an operating metric.
    
    Args:
        key: The metric key to retrieve
        
    Returns:
        The metric value
        
    Raises:
        KeyError: If the metric key doesn't exist
    """
    return OPERATING_METRICS[key]

def get_input_range(key: str) -> Tuple[int, int]:
    """
    Safely retrieve an input range.
    
    Args:
        key: The range key to retrieve
        
    Returns:
        Tuple of (min, max) values
        
    Raises:
        KeyError: If the range key doesn't exist
    """
    return INPUT_RANGES[key]