from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets , status
from .models import User , Message , UserSubscription , SubscriptionPlan , Task
from django.utils.timezone import now
from .serializers import ProfitCalculatorSerializer , MessageSerializer , LaborLawCalculatorSerializer , SocialSecurityCalculatorSerializer
from .tax_calculator import (
    calculate_income_tax,
    calculate_corporate_tax,
    calculate_personal_business_tax,
    calculate_dividend_tax,
    calculate_contractor_tax,
    calculate_declaration_penalty,
    calculate_vat_sales,
    calculate_vat_import,
    calculate_vat_delay_penalty,
    calculate_property_rent_tax,
    calculate_property_transfer_tax,
    calculate_property_construction_sale_tax,
    calculate_heir_share,
    calculate_inheritance_tax,
    calculate_customs_tax,
    calculate_raw_material_import_tax,
    calculate_equipment_import_tax,
    calculate_export_tax,
    calculate_withholding_contractor_tax,
    calculate_personal_service_tax,
    calculate_correction_penalty,
    calculate_quarterly_tax,
    calculate_annual_tax,
    calculate_payment_delay_penalty,   
)
from .LaborLawCalculators import (
    Basic_salary_based_on_working_hours,
    Overtime_And_workOnPublicHolidays,
    nightwork,
    shift_right,
    eid,
    performance_bonus,
    years_of_work,
    unused_paid_leave,
    Salary_for_leave_without,
    sick_leave,
    Travel_allowance,
    Housing_allowance,
    Grocery_allowance,
    Late_payment_crimes,
    Overdue_insurance_penalty,
    Compensation_for_contract_termination
)
from .SocialSecurityCalculators import (
    self_empleyed_insurance,
    workers_insurance,
    unemployment_insurance ,
    Retirement_pension ,
    delaySendingList ,
    delayPayment ,
    Insured_share ,
    termination_bonus
    )
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import UserSerializer , AllUsers , TaskSerializer
from datetime import timedelta


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Use the serializer to create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Retrieve tokens from the serializer's context
        tokens = serializer.context.get('tokens')

        # Build the response
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED, headers=headers)


class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all() 
    serializer_class = AllUsers

class SendMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipient_id = request.data.get('recipient')
        body = request.data.get('body')

        if recipient_id == request.user.id :
            return Response(
                {'error' : 'You can not message to yourself !'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Recipient does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = Message.objects.create(
            recipient=recipient,
            body=body
        )
        return Response(
            {
                'id': message.id,
                'recipient': recipient.username,
                'body': message.body,
                'read' : message.read ,
                'created_at': message.created_at
            },
            status=status.HTTP_201_CREATED
        )

class GetUserMessagesView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user
        messages = Message.objects.filter(recipient=user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
class ChangeSubscriptionPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        plan_name = request.data.get('plan')

        try:
            plan = SubscriptionPlan.objects.get(name=plan_name)
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Invalid plan name'}, status=status.HTTP_400_BAD_REQUEST)

        user_subscription = user.subscription
        user_subscription.plan = plan
        user_subscription.end_date = now() + timedelta(plan.duration)
        user_subscription.save()

        return Response({
            'message': f'Successfully changed to {plan.name.capitalize()} plan',
            'plan': plan.name,
            'end_date': user_subscription.end_date
        }, status=status.HTTP_200_OK)
    

class TaskViewList(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


#ONLINE CALCULATOR
class ProfitCalculatorViewSet(ViewSet):
    def create(self, request):
        serializer = ProfitCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = {}

            tax_fields = {
                'salary': ('income_tax', calculate_income_tax),
                'corporate_profit': ('corporate_tax', calculate_corporate_tax),
                'personal_profit': ('personal_business_tax', calculate_personal_business_tax),
                'dividend': ('dividend_tax', calculate_dividend_tax),
                'contract_value': ('contractor_tax', calculate_contractor_tax),
                'sales_value': ('vat_sales', calculate_vat_sales),
                'import_value': ('vat_import', calculate_vat_import),
                'customs_value': ('customs_tax', calculate_customs_tax),
                'raw_material_import_value': ('raw_material_import_tax', calculate_raw_material_import_tax),
                'equipment_import_value': ('equipment_import_tax', calculate_equipment_import_tax),
                'export_value': ('export_tax', calculate_export_tax),
                'delay_days': ('vat_delay_penalty', calculate_vat_delay_penalty),
                'rent_income': ('property_rent_tax', calculate_property_rent_tax),
                'transfer_value': ('property_transfer_tax', calculate_property_transfer_tax),
                'construction_sale_value': ('property_construction_sale_tax', calculate_property_construction_sale_tax),
                'contractor_income': ('withholding_contractor_tax', calculate_withholding_contractor_tax),
                'personal_service_income': ('personal_service_tax', calculate_personal_service_tax),
                'declaration_missing_days': ('declaration_penalty', calculate_declaration_penalty),
                'tax_payment_delay_days': ('payment_delay_penalty', calculate_payment_delay_penalty),
                'correction_penalty_amount': ('correction_penalty', calculate_correction_penalty),
                'quarterly_income': ('quarterly_tax', calculate_quarterly_tax),
                'total_annual_income': ('annual_tax', lambda x: calculate_annual_tax(x, data.get('paid_taxes', 0))),
            }


            for field, (response_key, calc_method) in tax_fields.items():
                value = data.get(field, 0)
                if value and calc_method:
                    response_data[response_key] = calc_method(value)

            # Handle special cases
            if data.get('inheritance_value', 0) > 0 and data.get('heir_share_percentage', 0) > 0:
                heir_share = calculate_heir_share(data['inheritance_value'], data['heir_share_percentage'])
                response_data['heir_share'] = heir_share
                response_data['inheritance_tax'] = calculate_inheritance_tax(heir_share)

            if data.get('rural_insurance_exemption'):
                response_data['rural_insurance_exemption'] = "معافیت مشتركان بیمه روستایی"

            if data.get('free_zone_exemption'):
                response_data['free_zone_exemption'] = "معافیت مشتركان منطقه آزاد"

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class LaborLawCalculatorViewSet(ViewSet):
    def create(self , request):
        serializer = LaborLawCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = {}
            
            if data.get('salary') > 0 :
                response_data['basic_salary'] = Basic_salary_based_on_working_hours(data['salary'])

            elif data.get("hourscount") > 0 and data.get("salaryvalueperhour") > 0:
                response_data['overtime_amount'] = Overtime_And_workOnPublicHolidays(data["salaryvalueperhour"] , data['hourscount'])
                response_data['night_shift_amount'] = nightwork(data["salaryvalueperhour"] , data['hourscount'])

            elif data.get("hourscount") > 0 and data.get("salaryvaluepermounth") > 0 and data.get("shiftvalue") > 0:
                response_data['shift_right'] = shift_right(data["salaryvaluepermounth"] , data['shiftvalue'] , data['hourscount'])
                
            elif data.get("basicsalaryvaluepermounth") > 0 and data.get("workedmonth") > 0:
                response_data['eid_amount'] = eid(data["basicsalaryvaluepermounth"] , data['workedmonth'])

            elif data.get("percentageOFbonus") > 0 and data.get("basicsalaryvaluepermounth") > 0:
                response_data['performance_bonus_amount'] = performance_bonus(data["basicsalaryvaluepermounth"] , data['percentageOFbonus'])

            elif data.get("basicsalaryvaluepermounth") > 0 and data.get("workedmounthcount") > 0:
                response_data['years_of_work_amount'] = years_of_work(data["basicsalaryvaluepermounth"] , data['workedmounthcount'])

            elif data.get("marriedOrnot") and data.get("totaldays") > 0 and data.get("salaryvalueperday") > 0:
                response_data['sick_leave_days'] = sick_leave(data["marriedOrnot"] , data['totaldays'] , data['salaryvalueperday'])

            elif data.get("totaldays") > 0 and data.get("salaryvalueperday") > 0:
                response_data['unused_paid_leave'] = unused_paid_leave(data["salaryvalueperday"] , data['totaldays'])
                response_data['Salary_for_leave_without'] = Salary_for_leave_without(data["salaryvalueperday"] , data['totaldays'])

            elif data.get("realtime") > 0 and data.get("legaltime") > 0 and data.get("approvedvalue") > 0:
                response_data['travel_allowance_amount'] = Travel_allowance(data["realtime"] , data["legaltime"] , data['approvedvalue'])
                response_data['grocery_allowance_amount'] = Grocery_allowance(data["realtime"] , data["legaltime"] , data['approvedvalue'])
           
            elif data.get("salaryvaluepermonth") > 0 and data.get("totaldays") > 0:
                response_data['late_payment_crimes_amount'] = Late_payment_crimes(data["salaryvaluepermonth"] , data['totaldays'])

            elif data.get("oip") > 0 and data.get("totalmonth") > 0:
                response_data['overdue_insurance_penalty_amount'] = Overdue_insurance_penalty(data["oip"] , data['totalmonth'])

            elif data.get("salaryvaluepermonth") > 0 and data.get("remainingTime") > 0 and data.get("Arrears"):
                response_data['compensation_for_contract_termination_amount'] = Compensation_for_contract_termination(data['remainingTime'] , data['salaryvaluepermonth'] , data["Arrears"])
            
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                                            



class SocialSecurityculatorViewSet(ViewSet):
    def create(self , request):
        serializer = SocialSecurityCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = {}
            
            if data.get('salary') > 0 and data.get('rate') > 0 :
                response_data['self_empleyed_insurance'] = self_empleyed_insurance(data['salary'] , data['rate'])

            elif data.get("variable_benefits") > 0:
                response_data['workers_insurance'] = workers_insurance(data["variable_benefits"])

            elif data.get("workHistory") > 0 and data.get("countUnderTutelage") > 0 and data.get("average_salary_inPast90days") > 0:
                response_data['unemployment_insurance'] = unemployment_insurance(data["workHistory"] , data.get('MarriedOrNot') , data['countUnderTutelage'] , data['average_salary_inPast90days'])
                
            elif data.get("avaragelast2yearsSalary") > 0 and data.get("insurance_history") > 0:
                response_data['Retirement_pension'] = Retirement_pension(data["avaragelast2yearsSalary"] , data['insurance_history'])

            elif data.get("right_insurance") > 0 and data.get("monthdelay") > 0:
                response_data['right_insurance_delay_amount'] = delayPayment(data["right_insurance"] , data['monthdelay'])

            elif data.get("right_insurance") > 0:
                response_data['right_insurance'] = delaySendingList(data["right_insurance"])

            elif data.get("treatment_cost") > 0 and data.get("insured_share") > 0 and data.get("peyment_ceiling"):
                response_data['insured_share_amount'] = Insured_share(data["insured_share"] , data['peyment_ceiling'] , data['treatment_cost'])

            elif data.get("lastmonthsalary") and data.get("yearsofWork") > 0 :
                response_data['termination_bonus_amount'] = termination_bonus(data["lastmonthsalary"] , data['yearsofWork'])
            
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)