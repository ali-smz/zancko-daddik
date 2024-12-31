from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets , status
from .models import User
from .serializers import ProfitCalculatorSerializer
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
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import UserSerializer , AllUsers

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all() 
    serializer_class = AllUsers

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

            # Calculate taxes for relevant fields
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
    

    
    