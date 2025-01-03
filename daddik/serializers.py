from rest_framework import serializers
from .models import User , Message



class AllUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  


class MessageSerializer(serializers.ModelSerializer):
     class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'body', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = { 'password': {'write_only': True} }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            lastName=validated_data.get('lastName', ''),
            profilePicture=validated_data.get('profilePicture', None),
            lable=validated_data.get('lable', 'unknown'),
            job=validated_data.get('job', ''),
            national_code=validated_data.get('national_code', None),
            address=validated_data.get('address', ''),
            workNumber=validated_data.get('workNumber', None),
            role=validated_data.get('role', ''),
            companyName=validated_data.get('companyName', ''),
            companyNationalId=validated_data.get('companyNationalId', None),
            document=validated_data.get('document', None),
            officialNewspaper=validated_data.get('officialNewspaper', None),
            companyWebsite=validated_data.get('companyWebsite', ''),
            companyEmail=validated_data.get('companyEmail', ''),
            connectorName=validated_data.get('connectorName', ''),
            connectorLastname=validated_data.get('connectorLastname', ''),
            connectorNationalCode=validated_data.get('connectorNationalCode', ''),
            connectorPhoneNumber=validated_data.get('connectorPhoneNumber', ''),
            connectorRole=validated_data.get('connectorRole', ''),
            introductionLetter=validated_data.get('introductionLetter', None),
            stars=validated_data.get('stars', 0),
            searchs=validated_data.get('searchs', 0),
            billsNumber=validated_data.get('billsNumber', 0),
            isPremium=validated_data.get('isPremium', False),
        )
        return user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'name': instance.name,
            'lastName': instance.lastName,
            'profilePicture': instance.profilePicture.url if instance.profilePicture else None,
            'lable': instance.lable,
            'job': instance.job,
            'national_code': instance.national_code,
            'address': instance.address,
            'workNumber': instance.workNumber,
            'role': instance.role,
            'companyName': instance.companyName,
            'companyNationalId': instance.companyNationalId,
            'document': instance.document.url if instance.document else None,
            'officialNewspaper': instance.officialNewspaper.url if instance.officialNewspaper else None,
            'companyWebsite': instance.companyWebsite,
            'companyEmail': instance.companyEmail,
            'connectorName': instance.connectorName,
            'connectorLastname': instance.connectorLastname,
            'connectorNationalCode': instance.connectorNationalCode,
            'connectorPhoneNumber': instance.connectorPhoneNumber,
            'connectorRole': instance.connectorRole,
            'introductionLetter': instance.introductionLetter.url if instance.introductionLetter else None,
            'stars': instance.stars,
            'searchs': instance.searchs,
            'billsNumber': instance.billsNumber,
            'isPremium': instance.isPremium,
            'createdAt': instance.createdAt,
            'updatedAt': instance.updatedAt,
        }
        



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
    

