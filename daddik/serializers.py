from rest_framework import serializers
from .models import User , Message
from django.utils.timezone import now
from .models import SubscriptionPlan , UserSubscription , Task
from datetime import timedelta



class MessageSerializer(serializers.ModelSerializer):
     class Meta:
        model = Message
        fields = '__all__'


class AllUsers(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField() 
    task_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'  
    
    def get_subscription(self, instance):
        if hasattr(instance, 'subscription'):
            return {
                'plan': instance.subscription.plan.name,
                'start_date': instance.subscription.start_date,
                'end_date': instance.subscription.end_date,
                'is_active': instance.subscription.is_active()
            }
        return None
    
    def get_task_count(self , instance) : 
        return instance.tasks.filter(completed=False).count()


class UserSerializer(serializers.ModelSerializer):
    referral_code = serializers.ReadOnlyField()  # Ensure referral code is not user-editable
    referred_by_code = serializers.CharField(write_only=True, required=False)
    messages = MessageSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField() 
    task_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = { 'password': {'write_only': True} }

    def get_subscription(self, instance):
        if hasattr(instance, 'subscription'):
            return {
                'plan': instance.subscription.plan.name,
                'start_date': instance.subscription.start_date,
                'end_date': instance.subscription.end_date,
                'is_active': instance.subscription.is_active()
            }
        return None
    
    def get_task_count(self , instance) :
        return instance.tasks.filter(completed = False).count()
    

    def create(self, validated_data):
        try:
            default_plan = SubscriptionPlan.objects.get(name='free')
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("The 'free' subscription plan is missing.")
        
        referred_by_code = validated_data.pop('referred_by_code', None)
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

        UserSubscription.objects.create(
            user=user,
            plan=default_plan,
            start_date=now(),
            end_date=now() + timedelta(default_plan.duration)
        )


        if referred_by_code:
            try:
                referrer = User.objects.get(referral_code=referred_by_code)
                user.referred_by = referrer
                user.save()

                referrer.referral_count += 1
                referrer.save()
            except User.DoesNotExist:
                pass  

        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profilePicture'] = (
            instance.profilePicture.url if instance.profilePicture else None
        )
        representation['document'] = (
            instance.document.url if instance.document else None
        )
        representation['officialNewspaper'] = (
            instance.officialNewspaper.url if instance.officialNewspaper else None
        )
        representation['introductionLetter'] = (
            instance.introductionLetter.url if instance.introductionLetter else None
        )
        representation['referral_code'] = instance.referral_code
        if instance.referred_by:
            representation['referred_by'] = {
                'id': instance.referred_by.id,
                'username': instance.referred_by.username,
                'referral_code': instance.referred_by.referral_code,
            }
        else:
            representation['referred_by'] = None
        representation['referral_count'] = instance.referral_count

        representation['messages'] = MessageSerializer(instance.messages.all(), many=True).data
        return representation
        

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'completed', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Task.objects.create(user=user, **validated_data) 



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