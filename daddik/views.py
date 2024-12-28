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
            export_value = serializer.validated_data.get('export_value', 0)  # مقدار صادرات
            raw_material_import_value = serializer.validated_data.get('raw_material_import_value', 0)  # واردات مواد اولیه
            equipment_import_value = serializer.validated_data.get('equipment_import_value', 0)  # واردات تجهیزات
            delay_days = serializer.validated_data.get('delay_days', 0)
            rent_income = serializer.validated_data.get('rent_income', 0)
            transfer_value = serializer.validated_data.get('transfer_value', 0)
            construction_sale_value = serializer.validated_data.get('construction_sale_value', 0)
            inheritance_value = serializer.validated_data.get('inheritance_value', 0)
            heir_share_percentage = serializer.validated_data.get('heir_share_percentage', 0)


            

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
            if raw_material_import_value > 0:
                response_data['raw_material_import_tax'] = self.calculate_raw_material_import_tax(raw_material_import_value)
            if equipment_import_value > 0:
                response_data['equipment_import_tax'] = self.calculate_equipment_import_tax(equipment_import_value)
            if export_value > 0:
                response_data['export_tax'] = self.calculate_export_tax(export_value)
            if delay_days > 0:
                response_data['vat_delay_penalty'] = self.calculate_vat_delay_penalty(delay_days)
            if rent_income > 0:
                response_data['property_rent_tax'] = self.calculate_property_rent_tax(rent_income)
            if transfer_value > 0:
                response_data['property_transfer_tax'] = self.calculate_property_transfer_tax(transfer_value)
            if construction_sale_value > 0:
                response_data['property_construction_sale_tax'] = self.calculate_property_construction_sale_tax(construction_sale_value)
            if inheritance_value > 0 and heir_share_percentage > 0:
                heir_share = self.calculate_heir_share(inheritance_value, heir_share_percentage)
                response_data['heir_share'] = heir_share
                response_data['inheritance_tax'] = self.calculate_inheritance_tax(heir_share)





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
    
     # محاسبه مالیات اجاره املاک
    def calculate_property_rent_tax(self, rent_income):
        tax_rate = 0.15 
        return rent_income * tax_rate
    
    # محاسبه مالیات نقل‌وانتقال املاک
    def calculate_property_transfer_tax(self, transfer_value):
        tax_rate = 0.05 
        return transfer_value * tax_rate
    
    # محاسبه مالیات بر ساخت و فروش املاک
    def calculate_property_construction_sale_tax(self, construction_sale_value):
        tax_rate = 0.20 
        return construction_sale_value * tax_rate
    
    # محاسبه سهم وارث
    def calculate_heir_share(self, inheritance_value, heir_share_percentage):
        return (inheritance_value * heir_share_percentage) / 100

    # محاسبه مالیات بر ارث
    def calculate_inheritance_tax(self, heir_share):
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
    def calculate_customs_tax(self, import_value):
        customs_tax_rate = 0.05  # نرخ مالیات گمرکی
        return import_value * customs_tax_rate

    # مالیات بر واردات مواد اولیه
    def calculate_raw_material_import_tax(self, raw_material_import_value):
        raw_material_tax_rate = 0.08  # نرخ مالیات واردات مواد اولیه
        return raw_material_import_value * raw_material_tax_rate

    # مالیات بر واردات تجهیزات
    def calculate_equipment_import_tax(self, equipment_import_value):
        equipment_tax_rate = 0.10  # نرخ مالیات واردات تجهیزات
        return equipment_import_value * equipment_tax_rate

    # مالیات صادرات
    def calculate_export_tax(self, export_value):
        export_tax_rate = 0.04  # نرخ مالیات صادرات
        return export_value * export_tax_rate
    
    