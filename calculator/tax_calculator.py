
# INCOME TAX
def calculate_income_tax(salary):
    if salary <= 56000000:
        return 0
    elif salary <= 150000000:
        return (salary - 56000000) * 0.1
    elif salary <= 300000000:
        return (salary - 150000000) * 0.15 + 9400000
    else:
        return (salary - 300000000) * 0.25 + 31900000

# شرکت های حقوقی
def calculate_corporate_tax(profit):
    return profit * 0.25

# شرکت های حقیقی
def calculate_personal_business_tax(profit):
    if profit <= 300000000:
        return profit * 0.15
    elif profit <= 1000000000:
        return (profit - 300000000) * 0.20 + 45000000
    else:
        return (profit - 1000000000) * 0.25 + 195000000

# مالیات بر سود سهام
def calculate_dividend_tax(dividend):
    return dividend * 0.10

# مالیات بر درامد ‍‍‍‍‍‍‍پمانکاران
def calculate_contractor_tax(contract_value):
    return contract_value * 0.05

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
def calculate_vat_import(import_value):
    vat_rate = 0.09
    return import_value * vat_rate

# جریمه تأخیر در ارسال اظهارنامه ارزش افزوده
def calculate_vat_delay_penalty(delay_days):
    daily_penalty_rate = 0.02
    base_penalty = 1000000
    return base_penalty + (delay_days * daily_penalty_rate * base_penalty)

# محاسبه مالیات اجاره املاک
def calculate_property_rent_tax(rent_income):
    tax_rate = 0.15
    return rent_income * tax_rate

# محاسبه مالیات نقل‌وانتقال املاک
def calculate_property_transfer_tax(transfer_value):
    tax_rate = 0.05
    return transfer_value * tax_rate

# محاسبه مالیات بر ساخت و فروش املاک
def calculate_property_construction_sale_tax(construction_sale_value):
    tax_rate = 0.20
    return construction_sale_value * tax_rate

# محاسبه سهم وارث
def calculate_heir_share(inheritance_value, heir_share_percentage):
    return (inheritance_value * heir_share_percentage) / 100

# محاسبه مالیات بر ارث
def calculate_inheritance_tax(heir_share):
    real_estate_tax_rate = 0.05
    bank_deposit_tax_rate = 0.03
    securities_tax_rate = 0.02

    real_estate_tax = heir_share * real_estate_tax_rate
    bank_deposit_tax = heir_share * bank_deposit_tax_rate
    securities_tax = heir_share * securities_tax_rate

    return {
        'real_estate_tax': real_estate_tax,
        'bank_deposit_tax': bank_deposit_tax,
        'securities_tax': securities_tax
    }

# مالیات گمرکی
def calculate_customs_tax(import_value):
    customs_tax_rate = 0.05
    return import_value * customs_tax_rate

# مالیات بر واردات مواد اولیه
def calculate_raw_material_import_tax(raw_material_import_value):
    raw_material_tax_rate = 0.08
    return raw_material_import_value * raw_material_tax_rate

# مالیات بر واردات تجهیزات
def calculate_equipment_import_tax(equipment_import_value):
    equipment_tax_rate = 0.10
    return equipment_import_value * equipment_tax_rate

# مالیات صادرات
def calculate_export_tax(export_value):
    export_tax_rate = 0.04
    return export_value * export_tax_rate

# محاسبه مالیات قرارداد های پیمانکاری
def calculate_withholding_contractor_tax(contractor_income):
    tax_rate = 0.05
    return contractor_income * tax_rate

# محاسبه مالیات بر درآمد پزشکان، مشاوران، و افراد حقیقی
def calculate_personal_service_tax(personal_service_income):
    tax_rate = 0.10
    return personal_service_income * tax_rate


def calculate_correction_penalty(correction_amount):
    penalty_rate = 0.1
    return correction_amount * penalty_rate


def calculate_quarterly_tax(quarterly_income):
    tax_rate = 0.09
    return quarterly_income * tax_rate


def calculate_annual_tax(total_income, paid_taxes):
    tax_rate = 0.2
    annual_tax = total_income * tax_rate
    net_tax = annual_tax - paid_taxes
    return max(net_tax, 0)


def calculate_payment_delay_penalty(delay_days):
    base_penalty = 2000000
    daily_penalty_rate = 0.025
    if delay_days <= 0:
        return 0
    total_penalty = base_penalty + (delay_days * daily_penalty_rate * base_penalty)
    return total_penalty
