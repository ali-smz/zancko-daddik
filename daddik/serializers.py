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
    delay_days = serializers.IntegerField(required=False, default=0)