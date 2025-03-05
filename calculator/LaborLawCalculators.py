from datetime import datetime 

#حقوق پایه بر اساس ساعت کاری
def Basic_salary_based_on_working_hours(salary , monthly_worked , monthly_hours = 220 ):
    r = salary/monthly_hours
    r = r * monthly_worked
    return r

#اضافه‌کاری 
def Overtime_And_workOnPublicHolidays(salary, worked_hours, monthly_hours=220, overtime_percentage=40):
    if overtime_percentage < 40:
        overtime_percentage = 40
    hourly_rate = salary / monthly_hours
    overtime_rate = hourly_rate * (1 + overtime_percentage / 100)
    overtime_hours = max(0, worked_hours - monthly_hours)
    overtime_pay = overtime_rate * overtime_hours
    
    return overtime_pay

#شب کاری
def nightwork(salary,night_hours,monthly_hours=220 , night_shift_percentage = 35 ):
    if night_shift_percentage < 35:
        night_shift_percentage = 35
    hourly_rate = salary / monthly_hours
    night_shift_rate = hourly_rate * (1 + night_shift_percentage / 100)
    night_shift_pay = night_shift_rate * night_hours
    
    return night_shift_pay

#حق شیفت
def shift_right(hourscount,shiftvalue,salaryvaluepermounth):
    if shiftvalue == 2:
        r = hourscount * salaryvaluepermounth * 0.1
        return r
    elif shiftvalue == 3:
        r = hourscount * salaryvaluepermounth * 0.15
    else:
        return "Not Included"

#محاسبه عیدی
def eid(basicsalaryvaluepermounth,workedmonth):
    r1 = basicsalaryvaluepermounth * workedmonth/6
    r2 = basicsalaryvaluepermounth * workedmonth/4
    return rf"عیدی محاسبه شده بین {r1} و {r2} است"

#پاداش عملکرد
def performance_bonus(basicsalaryvaluepermounth,percentageOFbonus):
    return basicsalaryvaluepermounth * (percentageOFbonus / 100)

#محاسبه سنوات پایان کار
def years_of_work(basicsalaryvaluepermounth,workedmounthcount):
    return basicsalaryvaluepermounth * (workedmounthcount/12) * 0.5

#مرخصی استحقاقی استفاده نشده
def unused_paid_leave(totaldays,salaryvalueperday):
    return salaryvalueperday * totaldays

# مرخصی بدون حقوق
def Salary_for_leave_without(totaldaysUsed,salaryvalueperday):
    r = totaldaysUsed * salaryvalueperday
    return r

#مرخصی استعلاجی
def sick_leave(isConfiremed,totaldays,salaryvalueperday):
    if isConfiremed :
        r = totaldays * salaryvalueperday * 0.75
    else :
        r = totaldays * salaryvalueperday * 0.6666
    return r


#کمک‌هزینه ایاب‌وذهاب
def Travel_allowance(realtime,legaltime,approvedvalue):
    r = approvedvalue * (realtime/legaltime)
    return r

#کمک هزینه مسکن
def Housing_allowance(realtime,legaltime,approvedvalue):
    r = approvedvalue * (realtime/legaltime)
    return r

#کمک‌هزینه خواربار
def Grocery_allowance(realtime,legaltime,approvedvalue):
    r = approvedvalue * (realtime/legaltime)
    return r

#جرائم تأخیر در پرداخت حقوق
def Late_payment_crimes(salaryvaluepermonth,totaldays):
    payment_crime = salaryvaluepermonth * 0.1
    payment_crime2 = salaryvaluepermonth * 0.25
    r1 = totaldays * payment_crime
    r2 = totaldays * payment_crime2
    return  rf"جریمه محاسبه شده بین {r1} و {r2} است"

#محاسبه جریمه بیمه معوقه
def Overdue_insurance_penalty(oip,totalmonth):
    r = oip * 0.02 * totalmonth 
    return r

#جبران خسارت فسخ قرارداد
def Compensation_for_contract_termination(contract_amount, start_date, termination_date, total_duration_months, compensation_percentage):
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(termination_date, str):
        termination_date = datetime.strptime(termination_date, '%Y-%m-%d').date()

    elapsed_months = (termination_date.year - start_date.year) * 12 + (termination_date.month - start_date.month)
 
    elapsed_months = min(elapsed_months, total_duration_months)

    remaining_months = total_duration_months - elapsed_months
    

    if remaining_months <= 0:
        return 0    
    compensation = (contract_amount * compensation_percentage / 100) * (remaining_months / total_duration_months)
    return compensation

