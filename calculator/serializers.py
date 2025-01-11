from rest_framework import serializers


class ProfitCalculatorSerializer(serializers.Serializer):
    salary = serializers.IntegerField(required=False, default=0)
    corporate_profit = serializers.IntegerField(required=False, default=0)
    personal_profit = serializers.IntegerField(required=False, default=0)
    dividend = serializers.IntegerField(required=False, default=0)
    contract_value = serializers.IntegerField(required=False, default=0)
    sales_value = serializers.IntegerField(required=False, default=0) 
    import_value = serializers.IntegerField(required=False, default=0)
    export_value = serializers.IntegerField(required=False, default=0)  # مقدار صادرات
    raw_material_import_value = serializers.IntegerField(required=False, default=0)  # واردات مواد اولیه
    equipment_import_value = serializers.IntegerField(required=False, default=0)  # واردات تجهیزات
    delay_days = serializers.IntegerField(required=False, default=0)
    customs_value = serializers.IntegerField(required=False, default=0)
    rent_income = serializers.IntegerField(required=False, default=0) 
    transfer_value = serializers.IntegerField(required=False, default=0)    
    construction_sale_value = serializers.IntegerField(required=False, default=0)
    inheritance_value = serializers.IntegerField(required=False, default=0)  
    heir_share_percentage = serializers.IntegerField(required=False, default=0)
    contractor_income = serializers.IntegerField(required=False, default=0)  # درآمد قرارداد پیمانکاری
    personal_service_income = serializers.IntegerField(required=False, default=0)  # درآمد پزشکان، مشاوران، و افراد حقیقی
    declaration_missing_days = serializers.IntegerField(required=False, default=0)
    tax_payment_delay_days = serializers.IntegerField(required=False, default=0)
    rural_insurance_exemption = serializers.BooleanField(required=False, default=False)
    correction_penalty_amount = serializers.IntegerField(required=False, default=0)
    quarterly_income = serializers.IntegerField(required=False, default=0)
    total_annual_income = serializers.IntegerField(required=False, default=0)
    paid_taxes = serializers.IntegerField(required=False, default=0)
    free_zone_exemption = serializers.BooleanField(required=False, default=False)
    salary_exemption = serializers.BooleanField(required=False, default=False)
    


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