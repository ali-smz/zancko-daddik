def calculate_night_overtime(base_salary, standard_hours, night_overtime_hours):
    """
    Calculate night overtime pay based on the given inputs.

    Parameters:
        base_salary (float): Monthly base salary in Tomans.
        standard_hours (int): Standard monthly working hours.
        night_overtime_hours (int): Number of night overtime hours worked.

    Returns:
        float: Night overtime pay amount.
    """
    # Hourly rate calculation
    hourly_rate = base_salary / standard_hours
    
    # Night overtime rate (35% increase)
    night_overtime_rate = hourly_rate * 1.35
    
    # Night overtime pay
    night_overtime_pay = night_overtime_rate * night_overtime_hours
    
    return night_overtime_pay

def calculate_self_employment_insurance(base_salary, insurance_rate):
    """
    Calculate self-employment insurance based on the given inputs.

    Parameters:
        base_salary (float): Base salary for insurance calculation.
        insurance_rate (float): Insurance rate percentage (e.g., 12%, 14%, 18%).

    Returns:
        float: Self-employment insurance amount.
    """
    # Ensure the insurance rate is valid
    if insurance_rate not in [12, 14, 18]:
        raise ValueError("Insurance rate must be 12%, 14%, or 18%.")
    
    # Calculate insurance amount
    insurance_amount = base_salary * (insurance_rate / 100)
    
    return insurance_amount

def calculate_worker_insurance(insurable_salary):
    """
    Calculate worker insurance contributions based on the given inputs.

    Parameters:
        insurable_salary (float): Total insurable salary (base + allowances).

    Returns:
        dict: Worker and employer insurance contributions.
    """
    # Worker's share (7%)
    worker_share = insurable_salary * 0.07
    
    # Employer's share (23%)
    employer_share = insurable_salary * 0.23
    
    # Total insurance amount
    total_insurance = worker_share + employer_share
    
    return {
        "worker_share": worker_share,
        "employer_share": employer_share,
        "total_insurance": total_insurance
    }

def calculate_unemployment_insurance(avg_salary_last_3_months, dependents=0):
    """
    Calculate unemployment insurance based on the given inputs.

    Parameters:
        avg_salary_last_3_months (float): Average salary of the last 3 months.
        dependents (int): Number of dependents (default is 0).

    Returns:
        float: Unemployment insurance amount.
    """
    # Base percentage (55%)
    base_percentage = 0.55
    
    # Additional percentage per dependent (10% each, max 4 dependents)
    additional_percentage = min(dependents, 4) * 0.10
    
    # Total percentage
    total_percentage = base_percentage + additional_percentage
    
    # Cap at 80%
    total_percentage = min(total_percentage, 0.80)
    
    # Calculate unemployment insurance
    unemployment_insurance = avg_salary_last_3_months * total_percentage
    
    return unemployment_insurance


def calculate_pension(avg_salary_last_2_years, years_of_service):
    """
    Calculate retirement pension based on the given inputs.

    Parameters:
        avg_salary_last_2_years (float): Average salary of the last 2 years.
        years_of_service (int): Total years of service.

    Returns:
        float: Retirement pension amount.
    """
    # Pension formula
    pension = avg_salary_last_2_years * (years_of_service / 30)
    
    return pension


def calculate_insurance_delay_penalty(debt_amount, months_delayed):
    """
    Calculate penalty for delayed insurance payment.

    Parameters:
        debt_amount (float): Total insurance debt amount.
        months_delayed (int): Number of months delayed.

    Returns:
        float: Penalty amount.
    """
    # Monthly penalty rate (2%)
    penalty_rate = 0.02
    
    # Calculate penalty
    penalty = debt_amount * penalty_rate * months_delayed
    
    return penalty


def calculate_insurance_list_delay_penalty(total_insurance, months_delayed):
    """
    Calculate penalty for delayed submission of insurance list.

    Parameters:
        total_insurance (float): Total monthly insurance amount.
        months_delayed (int): Number of months delayed.

    Returns:
        float: Penalty amount.
    """
    # Monthly penalty rate (2%)
    penalty_rate = 0.02
    
    # Calculate penalty
    penalty = total_insurance * penalty_rate * months_delayed
    
    return penalty


def calculate_insured_share(total_cost, insured_percentage):
    """
    Calculate the insured person's share of medical costs.

    Parameters:
        total_cost (float): Total medical cost.
        insured_percentage (float): Percentage of cost covered by the insured.

    Returns:
        float: Insured person's share.
    """
    # Calculate insured share
    insured_share = total_cost * (insured_percentage / 100)
    
    return insured_share