from django.conf import settings

def calculate_income_tax(salary):
    
    if salary <= 56000000: 
        return 0
    elif salary <= 150000000:
        return (salary - 56000000) * 0.1  
    elif salary <= 300000000:
        return (salary - 150000000) * 0.15 + 9400000  
    else:
        return (salary - 300000000) * 0.25 + 31900000  


def calculate_corporate_tax(profit):
    return profit * 0.25  

def calculate_personal_business_tax(profit):
    
    if profit <= 300000000:
        return profit * 0.15  
    elif profit <= 1000000000:
        return (profit - 300000000) * 0.20 + 45000000 
    else:
        return (profit - 1000000000) * 0.25 + 195000000 

def calculate_dividend_tax(dividend):
    return dividend * 0.10 


def calculate_contractor_tax(contract_value):
    return contract_value * 0.05


if __name__ == "__main__":
    print(settings.ELASTICSEARCH_DSL)