from datetime import datetime


# INCOME TAX
def calculate_income_tax(gross_income , insurance_right , exemptions = 0):
    salary = gross_income - insurance_right - exemptions
    if salary <= 12000000:
        return 0
    elif salary <= 16500000 :
        return (salary - 12000000) * 0.1
    elif salary <= 27000000:
        return (salary - 16500000) * 0.15
    elif salary <= 40000000:
        return (salary - 27000000) * 0.2
    else:
        return (salary - 40000000) * 0.3


# شرکت های حقوقی
def calculate_corporate_tax(profit , taxPayer = 0):
    profit = profit - taxPayer
    return profit * 0.25

# شرکت های حقیقی
def calculate_personal_business_tax(profit):
    if profit <= 47500000:
        return 0
    elif profit <= 92500000:
        return (profit - 47500000) * 0.15
    elif profit <= 142500000:
        return (profit - 92500000) * 0.20
    else:
        return (profit - 142500000) * 0.25

# مالیات بر سود سهام
def calculate_dividend_tax(dividend):
    return dividend * 0.10

# مالیات بر درامد ‍‍‍‍‍‍‍پمانکاران
def calculate_contractor_tax(contract_value , prepaid , taxPayer = 0):
    salary = contract_value - taxPayer
    salary = salary * 0.25
    salary = salary - prepaid
    return salary

# تاخیر در اظهارنامه
def calculate_declaration_penalty(missing_days):
    daily_penalty_rate = 0.02
    base_penalty = 2000000
    return base_penalty + (missing_days * daily_penalty_rate * base_penalty)

# مالیات فروش کالا و خدمات
def calculate_vat_sales(sales_value):
    vat_rate = 0.09
    return sales_value * vat_rate

# مالیات ورودی کالاها
def calculate_vat_import(cif_value , import_value , other_comps = 0):
    custom_right = cif_value * 0.04
    trade_profit = cif_value * (import_value / 100)
    import_right = custom_right + trade_profit
    added_tax = (cif_value + import_right) * 0.09
    finalAmount = cif_value + import_right + added_tax + other_comps
    return finalAmount

# جریمه تأخیر در ارسال اظهارنامه ارزش افزوده
def calculate_vat_delay_penalty(delay_months , base_penalty):
    daily_penalty_rate = 0.02
    return base_penalty + (delay_months * daily_penalty_rate * base_penalty)

# محاسبه مالیات اجاره املاک
def calculate_property_rent_tax(rent_income, months, isLegal, costs=0):
    if isLegal:
        income = (rent_income * months) * 0.75
        if income < 24000000:
            income = income * 0.15
        elif income < 56000000:
            income = income * 0.2
        else:
            income = income * 0.25
    else:
        income = rent_income * months 
        income = income * 0.25

    income = income - costs
    return income



# محاسبه مالیات نقل‌وانتقال املاک
def calculate_property_transfer_tax(transfer_value):
    tax_rate = 0.05
    return transfer_value * tax_rate

# محاسبه مالیات بر ساخت و فروش املاک
def calculate_property_construction_sale_tax(construction_sale_value):
    tax_rate = 0.20
    return construction_sale_value * tax_rate

# محاسبه سهم وارث
def calculate_heir_share(inheritance_value, asset_type, relationship_class, number_of_heirs):
    tax_rate = 0

    if asset_type == 'property':
        if relationship_class == 1:
            tax_rate = 0.075  
        elif relationship_class == 2:
            tax_rate = 0.15  
        elif relationship_class == 3:
            tax_rate = 0.3  
    elif asset_type == 'cash':
        if relationship_class == 1:
            tax_rate = 0.03
        elif relationship_class == 2:
            tax_rate = 0.06 
        elif relationship_class == 3:
            tax_rate = 0.12 
    elif asset_type == 'car':
        if relationship_class == 1:
            tax_rate = 0.02 
        elif relationship_class == 2:
            tax_rate = 0.04 
        elif relationship_class == 3:
            tax_rate = 0.08  
    else:
        if relationship_class == 1:
            tax_rate = 0.1 
        elif relationship_class == 2:
            tax_rate = 0.2  
        elif relationship_class == 3:
            tax_rate = 0.4 

    inheritance_tax = inheritance_value * tax_rate
    tax_per_heir = inheritance_tax / number_of_heirs

    return inheritance_tax, tax_per_heir


# مالیات گمرکی
def calculate_customs_tax(cif_value, product_type):
    customs_rate = 0
    vat_rate = 0.09  
    excise_duty = 0 

    if product_type == 'electronic':
        customs_rate = 0.2  
    elif product_type == 'food':
        customs_rate = 0.05 
    elif product_type == 'machinery':
        customs_rate = 0.15
    else:
        customs_rate = 0.1 

    if product_type in ['luxury_goods', 'high_value_items']:
        excise_duty = 0.05  

    customs_tax = cif_value * customs_rate
    vat_tax = (cif_value + customs_tax) * vat_rate
    excise_tax = cif_value * excise_duty
    total_customs_tax = customs_tax + vat_tax + excise_tax

    return total_customs_tax, customs_tax, vat_tax, excise_tax


# مالیات بر واردات مواد اولیه
def calculate_raw_material_import_tax(cif_value, material_type):
    customs_rate = 0
    vat_rate = 0.09 
    excise_duty = 0  

    if material_type == 'metal':
        customs_rate = 0.05 
    elif material_type == 'chemical':
        customs_rate = 0.08 
    elif material_type == 'textile':
        customs_rate = 0.06 
    elif material_type == 'plastic':
        customs_rate = 0.07 
    elif material_type == 'wood':
        customs_rate = 0.04 
    else:
        customs_rate = 0.1 

    if material_type in ['chemical', 'plastic']:
        excise_duty = 0.03 

    customs_tax = cif_value * customs_rate
    vat_tax = (cif_value + customs_tax) * vat_rate
    excise_tax = cif_value * excise_duty
    total_import_tax = customs_tax + vat_tax + excise_tax

    return total_import_tax, customs_tax, vat_tax, excise_tax


# مالیات بر واردات تجهیزات
def calculate_equipment_import_tax(cif_value, equipment_type, customs_duty_rate, vat_rate=0.09, excise_duty_rate=0.0):
    customs_duty = cif_value * customs_duty_rate

    vat = (cif_value + customs_duty) * vat_rate

    excise_duty = cif_value * excise_duty_rate

    total_import_tax = customs_duty + vat + excise_duty

    return total_import_tax, customs_duty, vat, excise_duty


# مالیات صادرات
def calculate_export_tax(export_value , excise_duty_rate=0.0):
    excise_duty = export_value * excise_duty_rate
    total_export_tax = excise_duty

    return total_export_tax, excise_duty


# محاسبه مالیات قرارداد های پیمانکاری
def calculate_withholding_contractor_tax(contract_value  , project_type , tax_rate=0.1, vat_rate=0.09, excise_duty_rate=0.0):
    income_tax = contract_value * tax_rate
    vat_tax = contract_value * vat_rate
    excise_duty = contract_value * excise_duty_rate
    total_tax = income_tax + vat_tax + excise_duty

    return total_tax, income_tax, vat_tax, excise_duty

# محاسبه مالیات بر درآمد پزشکان، مشاوران، و افراد حقیقی
def calculate_personal_service_tax(income, job_type, exemptions=0, tax_rate=None):
    if job_type == 'doctor':
        exemptions += 10000000  
    elif job_type == 'consultant':
        exemptions += 5000000 
    
    taxable_income = income - exemptions
    if taxable_income <= 0:
        return 0 

    if tax_rate is None:
        if taxable_income <= 240000000:
            tax_rate = 0.15 
        elif taxable_income <= 560000000:
            tax_rate = 0.20 
        else:
            tax_rate = 0.25

    return taxable_income * tax_rate



def calculate_correction_penalty(initial_tax, amendment_date, initial_submission_date, penalty_rate_per_day=0.02):
    initial_submission_date = datetime.strptime(str(initial_submission_date), "%Y-%m-%d")
    amendment_date = datetime.strptime(str(amendment_date), "%Y-%m-%d")

    delay_days = (amendment_date - initial_submission_date).days
    
    if delay_days <= 0:
        return 0

    penalty = initial_tax * penalty_rate_per_day * delay_days
    return penalty



def calculate_quarterly_tax(income, tax_rate, exemptions=0):
    taxable_income = income - exemptions
 
    if taxable_income <= 0:
        return 0
    quarterly_tax = taxable_income * tax_rate

    return quarterly_tax


def calculate_annual_tax(income, exemptions=0, tax_brackets=None):
    if tax_brackets is None:
        tax_brackets = [
            (240000000, 0.15),
            (560000000, 0.20), 
            (float('inf'), 0.25)  
        ]

    taxable_income = income - exemptions
    
    if taxable_income <= 0:
        return 0

    total_tax = 0
    previous_limit = 0

    for limit, rate in tax_brackets:
        if taxable_income > previous_limit:
            taxable_at_this_rate = min(taxable_income, limit) - previous_limit
            total_tax += taxable_at_this_rate * rate
            previous_limit = limit
        else:
            break

    return total_tax


def calculate_payment_delay_penalty(tax_amount, due_date, payment_date, penalty_rate_per_day=0.02):
    if isinstance(due_date, str):
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
    if isinstance(payment_date, str):
        payment_date = datetime.strptime(payment_date, "%Y-%m-%d")

    days_delayed = (payment_date - due_date).days

    if days_delayed <= 0:
        return 0

    penalty = tax_amount * penalty_rate_per_day * days_delayed
    return penalty
