from rest_framework import serializers


class ProfitCalculatorSerializer(serializers.Serializer):
    gross_income = serializers.IntegerField(required=False, default=0)
    insurance_right = serializers.IntegerField(required=False, default=0)
    exemptions = serializers.IntegerField(required=False, default=0)
    taxPayer = serializers.IntegerField(required=False, default=0)
    corporate_profit = serializers.IntegerField(required=False, default=0)
    personal_profit = serializers.IntegerField(required=False, default=0)
    dividend = serializers.IntegerField(required=False, default=0)
    prepaid = serializers.IntegerField(required=False, default=0)
    sales_value = serializers.IntegerField(required=False, default=0) 
    import_value = serializers.IntegerField(required=False, default=0)
    cif_value = serializers.IntegerField(required=False, default=0)
    other_comps = serializers.IntegerField(required=False, default=0)

    raw_material_import_value = serializers.IntegerField(required=False, default=0)  # واردات مواد اولیه
    equipment_import_value = serializers.IntegerField(required=False, default=0)  # واردات تجهیزات
    delay_months = serializers.IntegerField(required=False, default=0)
    base_penalty = serializers.IntegerField(required=False, default=0)
    customs_value = serializers.IntegerField(required=False, default=0)
    rent_income = serializers.IntegerField(required=False, default=0) 
    months = serializers.IntegerField(required=False, default=0) 
    costs = serializers.IntegerField(required=False, default=0) 
    isLegal = serializers.BooleanField(required=False, default=False)

    inheritance_value = serializers.IntegerField(required=False, default=0)
    asset_type = serializers.ChoiceField(choices=['property', 'cash', 'car', 'other'], required=False)
    relationship_class = serializers.IntegerField(required=False, default=1) 
    number_of_heirs = serializers.IntegerField(required=False, default=1, min_value=1)
    
    cif_value = serializers.IntegerField(required=False, default=0) 
    product_type = serializers.ChoiceField(choices=['electronic', 'food', 'machinery', 'luxury_goods', 'high_value_items', 'other'], required=False)

    cif_value = serializers.IntegerField(required=False, default=0)
    material_type = serializers.ChoiceField(choices=['metal', 'chemical', 'textile', 'plastic', 'wood', 'other'], required=False)

    cif_value_equipment = serializers.IntegerField(required=False, default=0)
    equipment_type = serializers.ChoiceField(choices=['medical', 'industrial', 'electronics', 'other'], required=False)

    export_value = serializers.IntegerField(required=False, default=0)

    contract_value = serializers.IntegerField(required=False, default=0)
    project_type = serializers.ChoiceField(choices=['construction', 'IT', 'manufacturing', 'other'], required=False)

    personal_service_income = serializers.IntegerField(required=False, default=0)
    job_type = serializers.ChoiceField(choices=['doctor', 'consultant', 'freelancer', 'other'], required=False)

    initial_tax = serializers.IntegerField(required=False, default=0)
    amendment_date = serializers.DateField(required=False)
    initial_submission_date = serializers.DateField(required=False)


    quarterly_income = serializers.IntegerField(required=False, default=0)
    quarterly_tax_rate = serializers.FloatField(required=False, default=0.1)


    annual_income = serializers.IntegerField(required=False, default=0)

    tax_amount = serializers.IntegerField(required=False, default=0)
    due_date = serializers.DateField(required=False, allow_null=True)
    payment_date = serializers.DateField(required=False, allow_null=True)

    transfer_value = serializers.IntegerField(required=False, default=0)    
    construction_sale_value = serializers.IntegerField(required=False, default=0)
    inheritance_value = serializers.IntegerField(required=False, default=0)  
    heir_share_percentage = serializers.IntegerField(required=False, default=0)
    contractor_income = serializers.IntegerField(required=False, default=0)  # درآمد قرارداد پیمانکاری
    declaration_missing_days = serializers.IntegerField(required=False, default=0)
    tax_payment_delay_days = serializers.IntegerField(required=False, default=0)
    rural_insurance_exemption = serializers.BooleanField(required=False, default=False)
    correction_penalty_amount = serializers.IntegerField(required=False, default=0)
    quarterly_income = serializers.IntegerField(required=False, default=0)
    total_annual_income = serializers.IntegerField(required=False, default=0)
    paid_taxes = serializers.IntegerField(required=False, default=0)
    


class LaborLawCalculatorSerializer(serializers.Serializer):
    salary = serializers.IntegerField(required=False, default=0)
    hourscount = serializers.IntegerField(required=False, default=0)
    salaryvalueperhour = serializers.IntegerField(required=False, default=0)
    shiftvalue = serializers.IntegerField(required=False, default=0)
    salaryvaluepermounth = serializers.IntegerField(required=False, default=0)
    basicsalaryvaluepermounth = serializers.IntegerField(required=False, default=0) 
    workedmonth = serializers.IntegerField(required=False, default=0)
    percentageOFbonus = serializers.IntegerField(required=False, default=0) 
    workedmounthcount = serializers.IntegerField(required=False, default=0)
    totaldays = serializers.IntegerField(required=False, default=0) 
    salaryvalueperday = serializers.IntegerField(required=False, default=0)
    realtime = serializers.IntegerField(required=False, default=0)
    legaltime = serializers.IntegerField(required=False, default=0) 
    approvedvalue = serializers.IntegerField(required=False, default=0)    
    salaryvaluepermonth = serializers.IntegerField(required=False, default=0)
    totalmonth = serializers.IntegerField(required=False, default=0)  
    oip = serializers.IntegerField(required=False, default=0)
    remainingTime = serializers.IntegerField(required=False, default=0) 
    Arrears = serializers.IntegerField(required=False, default=0) 
    marriedOrnot = serializers.BooleanField(required=False, default=False)


class SocialSecurityCalculatorSerializer(serializers.Serializer):
    salary = serializers.IntegerField(required=False, default=0)
    rate = serializers.IntegerField(required=False, default=0)
    variable_benefits = serializers.IntegerField(required=False, default=0)
    workHistory = serializers.IntegerField(required=False, default=0)
    countUnderTutelage = serializers.IntegerField(required=False, default=0)
    average_salary_inPast90days = serializers.IntegerField(required=False, default=0) 
    avaragelast2yearsSalary = serializers.IntegerField(required=False, default=0)
    insurance_history = serializers.IntegerField(required=False, default=0) 
    right_insurance = serializers.IntegerField(required=False, default=0)
    monthdelay = serializers.IntegerField(required=False, default=0) 
    treatment_cost = serializers.IntegerField(required=False, default=0)
    insured_share = serializers.IntegerField(required=False, default=0)
    peyment_ceiling = serializers.IntegerField(required=False, default=0) 
    lastmonthsalary = serializers.IntegerField(required=False, default=0)    
    yearsofWork = serializers.IntegerField(required=False, default=0)
    marriedOrnot = serializers.BooleanField(required=False, default=False)