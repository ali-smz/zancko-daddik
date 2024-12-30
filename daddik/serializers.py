from rest_framework import serializers
from .models import LegalPerson , RealPerson

class RealPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealPerson
        fields = '__all__'


class LegalPersonSerializer(serializers.ModelSerializer):
    def validate_pdf(value):
        # volume limitation should be here 
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value
    
    document = serializers.FileField(validators=[validate_pdf])
    officialNewspaper = serializers.FileField(validators=[validate_pdf])
    introductionLetter = serializers.FileField(validators=[validate_pdf])

    class Meta:
        model = LegalPerson
        fields = '__all__'


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
    

