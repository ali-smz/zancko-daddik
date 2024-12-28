from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets , status
from .models import LegalPerson , RealPerson
from .serializers import RealPersonSerializer ,  LegalPersonSerializer , ProfitCalculatorSerializer

# Create your views here.
class RealPersonViewSet(viewsets.ModelViewSet):
    queryset = RealPerson.objects.all()
    serializer_class = RealPersonSerializer


class LegalPersonViewSet(viewsets.ModelViewSet):
    queryset = LegalPerson.objects.all()
    serializer_class = LegalPersonSerializer

#ONLINE CALCULATOR
class ProfitCalculatorViewSet(ViewSet):
    def create(self, request):
        serializer = ProfitCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            salary = serializer.validated_data.get('salary', 0)
            corporate_profit = serializer.validated_data.get('corporate_profit', 0)
            personal_profit = serializer.validated_data.get('personal_profit', 0)
            dividend = serializer.validated_data.get('dividend', 0)
            contract_value = serializer.validated_data.get('contract_value', 0)
            sales_value = serializer.validated_data.get('sales_value', 0)
            import_value = serializer.validated_data.get('import_value', 0)
            delay_days = serializer.validated_data.get('delay_days', 0)

            response_data = {}
            if salary > 0:
                response_data['income_tax'] = self.calculate_income_tax(salary)
            if corporate_profit > 0:
                response_data['corporate_tax'] = self.calculate_corporate_tax(corporate_profit)
            if personal_profit > 0:
                response_data['personal_business_tax'] = self.calculate_personal_business_tax(personal_profit)
            if dividend > 0:
                response_data['dividend_tax'] = self.calculate_dividend_tax(dividend)
            if contract_value > 0:
                response_data['contractor_tax'] = self.calculate_contractor_tax(contract_value)
            if sales_value > 0:
                response_data['vat_sales'] = self.calculate_vat_sales(sales_value)
            if import_value > 0:
                response_data['vat_import'] = self.calculate_vat_import(import_value)
            if delay_days > 0:
                response_data['vat_delay_penalty'] = self.calculate_vat_delay_penalty(delay_days)


            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # INCOME TAX
    def calculate_income_tax(self, salary):
        if salary <= 56000000:
            return 0
        elif salary <= 150000000:
            return (salary - 56000000) * 0.1
        elif salary <= 300000000:
            return (salary - 150000000) * 0.15 + 9400000
        else:
            return (salary - 300000000) * 0.25 + 31900000

    # شرکت های حقوقی 
    def calculate_corporate_tax(self, profit):
        return profit * 0.25
    
    # شرکت های حقیقی
    def calculate_personal_business_tax(self, profit):
        if profit <= 300000000:
            return profit * 0.15
        elif profit <= 1000000000:
            return (profit - 300000000) * 0.20 + 45000000
        else:
            return (profit - 1000000000) * 0.25 + 195000000
        
    # مالیات بر سود سهام 
    def calculate_dividend_tax(self, dividend):
        return dividend * 0.10

    # مالیات بر درامد ‍‍‍‍‍‍‍پمانکاران
    def calculate_contractor_tax(self, contract_value):
        return contract_value * 0.05
    
    # مالیات فروش کالا و خدمات
    def calculate_vat_sales(self, sales_value):
        vat_rate = 0.09 
        return sales_value * vat_rate
    
    # مالیات ورودی کالاها
    def calculate_vat_import(self, import_value):
        vat_rate = 0.09 
        return import_value * vat_rate

    # جریمه تأخیر در ارسال اظهارنامه ارزش افزوده
    def calculate_vat_delay_penalty(self, delay_days):
        daily_penalty_rate = 0.02 
        base_penalty = 1000000 
        return base_penalty + (delay_days * daily_penalty_rate * base_penalty)
    
    