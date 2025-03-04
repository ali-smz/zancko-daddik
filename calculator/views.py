from django.shortcuts import render
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
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import ProfitCalculatorSerializer , LaborLawCalculatorSerializer , SocialSecurityCalculatorSerializer


# Create your views here.

class ProfitCalculatorViewSet(ViewSet):
    def create(self, request):
        serializer = ProfitCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response_data = {}
            tax_fields = {
                'personal_profit': ('personal_business_tax', calculate_personal_business_tax),
                'dividend': ('dividend_tax', calculate_dividend_tax),
                'sales_value': ('vat_sales', calculate_vat_sales),
                'transfer_value': ('property_transfer_tax', calculate_property_transfer_tax),
                'construction_sale_value': ('property_construction_sale_tax', calculate_property_construction_sale_tax),
                'declaration_missing_days': ('declaration_penalty', calculate_declaration_penalty),
            }


            for field, (response_key, calc_method) in tax_fields.items():
                value = data.get(field, 0)
                if value and calc_method:
                    response_data[response_key] = calc_method(value)

            # Handle special cases
            if data.get('gross_income', 0) > 0 and data.get('insurance_right', 0) > 0:
                exemptions = data.get('exemptions', 0) 
                income_tax = calculate_income_tax(data['gross_income'], data['insurance_right'] , exemptions)
                response_data['income_tax'] = income_tax 

            if data.get('corporate_profit', 0) > 0 :
                taxPayer = data.get('taxPayer', 0) 
                corporate_tax = calculate_corporate_tax(data['corporate_profit'] , taxPayer)
                response_data['corporate_tax'] = corporate_tax 

            if data.get('contract_value', 0) > 0 and data.get('prepaid', 0) > 0:
                taxPayer = data.get('taxPayer', 0) 
                contracting_tax = calculate_contractor_tax(data['contract_value'], data['prepaid'] , taxPayer)
                response_data['contracting_tax'] = contracting_tax

            if data.get('import_value', 0) > 0 and data.get('cif_value', 0) > 0:
                other_comps = data.get('other_comps', 0) 
                vat_import = calculate_vat_import(data['import_value'], data['cif_value'] , other_comps)
                response_data['vat_import'] = vat_import

            if data.get('rent_income', 0) > 0 and data.get('months', 0) > 0:
                costs = data.get('costs', 0) 
                isLegal = data.get('isLegal', False)  # Ensure we always get this value
                property_rent_tax = calculate_property_rent_tax(data['rent_income'], data['months'], isLegal, costs)
                response_data['property_rent_tax'] = property_rent_tax

            if data.get('base_penalty', 0) > 0 and data.get('delay_months', 0) > 0:
                vat_delay_penalty = calculate_vat_delay_penalty(data['base_penalty'], data['delay_months'])
                response_data['vat_delay_penalty'] = vat_delay_penalty

            if data.get('inheritance_value', 0) > 0 and data.get('asset_type') and data.get('relationship_class'):
                inheritance_value = data['inheritance_value']
                asset_type = data['asset_type']
                relationship_class = data['relationship_class']
                number_of_heirs = data.get('number_of_heirs', 1) 

                inheritance_tax, tax_per_heir = calculate_heir_share(
                    inheritance_value, asset_type, relationship_class, number_of_heirs
                )

                response_data['inheritance_tax'] = inheritance_tax
                response_data['tax_per_heir'] = tax_per_heir

            if data.get('cif_value', 0) > 0 and data.get('product_type'):
                cif_value = data['cif_value']
                product_type = data['product_type']
                country_of_origin = data.get('country_of_origin', "")

                total_customs_tax, customs_tax, vat_tax, excise_tax = calculate_customs_tax(
                    cif_value, product_type, country_of_origin
                )

                response_data['total_customs_tax'] = total_customs_tax
                response_data['customs_tax'] = customs_tax
                response_data['vat_tax'] = vat_tax
                response_data['excise_tax'] = excise_tax


            if data.get('cif_value', 0) > 0 and data.get('material_type'):
                cif_value = data['cif_value']
                material_type = data['material_type']

                total_import_tax, customs_tax, vat_tax, excise_tax = calculate_raw_material_import_tax(
                    cif_value, material_type
                )

                response_data['total_raw_material_import_tax'] = total_import_tax
                response_data['customs_tax'] = customs_tax
                response_data['vat_tax'] = vat_tax
                response_data['excise_tax'] = excise_tax
            
            if data.get('cif_value_equipment', 0) > 0 and data.get('equipment_type'):
                cif_value = data['cif_value_equipment']
                equipment_type = data['equipment_type']

                equipment_duty_rates = {
                    'medical': 0.05,  
                    'industrial': 0.08,  
                    'electronics': 0.12, 
                    'other': 0.1  
                }

                customs_duty_rate = equipment_duty_rates.get(equipment_type, 0.1) 

                total_import_tax, customs_duty, vat, excise_duty = calculate_equipment_import_tax(
                    cif_value, equipment_type, customs_duty_rate
                )

                response_data['total_equipment_import_tax'] = total_import_tax
                response_data['customs_duty'] = customs_duty
                response_data['vat_tax'] = vat
                response_data['excise_tax'] = excise_duty

            if data.get('export_value', 0) > 0:
                export_value = data['export_value']
                default_excise_duty_rate = 0.02

                total_export_tax, excise_duty = calculate_export_tax(export_value, excise_duty_rate=default_excise_duty_rate)

                response_data['total_export_tax'] = total_export_tax
                response_data['excise_duty'] = excise_duty


            
            if data.get('contract_value', 0) > 0 and data.get('project_type'):
                contract_value = data['contract_value']
                project_type = data['project_type']

                project_tax_rates = {
                    'construction': 0.1,  
                    'IT': 0.07,  
                    'manufacturing': 0.08,  
                    'other': 0.1  
                }

                tax_rate = project_tax_rates.get(project_type, 0.1)

                total_tax, income_tax, vat_tax, excise_duty = calculate_withholding_contractor_tax(
                    contract_value, project_type, tax_rate
                )

                response_data['total_withholding_contractor_tax'] = total_tax
                response_data['income_tax'] = income_tax
                response_data['vat_tax'] = vat_tax
                response_data['excise_tax'] = excise_duty

            if data.get('personal_service_income', 0) > 0 and 'job_type' in data:
                personal_income = data['personal_service_income']
                job_type = data['job_type']
                exemptions = data.get('exemptions', 0)

                personal_service_tax = calculate_personal_service_tax(personal_income, job_type, exemptions)

                response_data['personal_service_tax'] = personal_service_tax

            if all(key in data for key in ['initial_tax', 'amendment_date', 'initial_submission_date']):
                initial_tax = data['initial_tax']
                amendment_date = data['amendment_date']
                initial_submission_date = data['initial_submission_date']

                correction_penalty = calculate_correction_penalty(initial_tax, amendment_date, initial_submission_date)

                response_data['correction_penalty'] = correction_penalty
                
            if data.get('quarterly_income', 0) > 0:
                quarterly_income = data['quarterly_income']
                quarterly_tax_rate = data.get('quarterly_tax_rate', 0.1)
                exemptions = data.get('exemptions', 0)

                quarterly_tax = calculate_quarterly_tax(quarterly_income, quarterly_tax_rate, exemptions)

                response_data['quarterly_tax'] = quarterly_tax

            if data.get('annual_income', 0) > 0:
                annual_income = data['annual_income']
                exemptions = data.get('exemptions', 0)

                annual_tax = calculate_annual_tax(annual_income, exemptions)

                response_data['annual_tax'] = annual_tax

            if all(key in data and data[key] is not None for key in ['tax_amount', 'due_date', 'payment_date']):
                tax_amount = data['tax_amount']
                due_date = data['due_date']
                payment_date = data['payment_date']

                payment_delay_penalty = calculate_payment_delay_penalty(tax_amount, due_date, payment_date)

                response_data['payment_delay_penalty'] = payment_delay_penalty

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