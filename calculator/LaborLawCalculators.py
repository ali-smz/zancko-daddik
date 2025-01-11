 
#حقوق پایه بر اساس ساعت کاری
def Basic_salary_based_on_working_hours(salary):
    r = salary/44
    return r

#اضافه‌کاری 
def Overtime_And_workOnPublicHolidays(hourscount,salaryvalueperhour):
    r = hourscount * salaryvalueperhour * 1.4
    return r

#شب کاری
def nightwork(hourscount,salaryvalueperhour):
    r = hourscount * salaryvalueperhour * 1.35
    return r

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
    return basicsalaryvaluepermounth * (workedmounthcount/12)

#مرخصی استحقاقی استفاده نشده
def unused_paid_leave(totaldays,salaryvalueperday):
    return salaryvalueperday * totaldays

# مرخصی بدون حقوق
def Salary_for_leave_without(totaldays,salaryvalueperday):
    r = totaldays * salaryvalueperday
    return r

#مرخصی استعلاجی
def sick_leave(marriedOrnot,totaldays,salaryvalueperday):
    if marriedOrnot :
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
    payment_crime = salaryvaluepermonth * 0.01
    payment_crime2 = salaryvaluepermonth * 0.015
    r1 = totaldays * payment_crime
    r2 = totaldays * payment_crime2
    return  rf"جریمه محاسبه شده بین {r1} و {r2} است"

#محاسبه جریمه بیمه معوقه
def Overdue_insurance_penalty(oip,totalmonth):
    r = oip * 0.02 * totalmonth 
    return r

#جبران خسارت فسخ قرارداد
def Compensation_for_contract_termination(salaryvaluepermonth,remainingTime,Arrears):
    r = (salaryvaluepermonth * remainingTime) + Arrears
    return r

#حقوق پایان خدمت برای هر سال خدمت
