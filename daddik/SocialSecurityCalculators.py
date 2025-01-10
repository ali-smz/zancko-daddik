import pandas as pd


data = pd.read_csv("Data_Calc.csv")
Insurance_rates = data.loc[data["sub"]=='Insurance rates' , 'value'].iloc[0]
base_insurance_salary = data.loc[data["sub"]=='base insurance salary' , 'value'].iloc[0]
right_treatment = data.loc[data["sub"]=='right treatment' , 'value'].iloc[0]
right_housing = data.loc[data["sub"]=='right housing' , 'value'].iloc[0]
Pension_ceiling = data.loc[data["sub"]=='Pension ceiling' , 'value'].iloc[0]
print(data.head())
#وبیمه رانندگان و مشاغل خاص و بیمه مشاغل آزاد
def self_empleyed_insurance(rate,salary):
    return right_treatment+(rate * salary)

#بیمه کارگران
def workers_insurance(Variable_benefits = 0):
    total = right_housing + right_treatment + base_insurance_salary + Variable_benefits
    rt = total * 0.30
    rworker = total * 0.07
    remployer = total * 0.2
    rgoverment = total * 0.03
    return rt,rworker,remployer,rgoverment

#بیمه بیکاری
def unemployment_insurance(workHistory,MarriedOrNot,countUnderTutelage,average_salary_inPast90days):
    period = 0
    if MarriedOrNot == "Not Married":
        if workHistory < 6:
            period = period
        elif 6 <= workHistory <24:
            period = period + 6
        elif 24 <= workHistory <120:
            period = period + 12
        elif 120 <= workHistory <180:
            period = period + 18
        elif 180 <=workHistory < 240:
            period = period + 26
        elif workHistory >= 240:
            period = period + 36
    if MarriedOrNot == "Married":
        if workHistory < 6:
            period = period
        elif 6 <= workHistory <24:
            period = period + 12
        elif 24 <= workHistory <120:
            period = period + 18
        elif 120 <= workHistory <180:
            period = period + 26
        elif 180 <=workHistory < 240:
            period = period + 36
        elif workHistory >= 240:
            period = period + 50
    r1 = average_salary_inPast90days * 0.55
    r2 = 0.1 * countUnderTutelage * average_salary_inPast90days
    rt = r1 + r2

    return rt, period

#مستمری بازنشستگی
def Retirement_pension(avaragelast2yearsSalary,Insurance_history):
    pension = 0
    if Insurance_history > 10:
        Insurance_history = Insurance_history - 10
        pension += 0.2
        newi =Insurance_history * 0.15
        pension += newi
        r = avaragelast2yearsSalary * pension
        if r > Pension_ceiling:
            r = Pension_ceiling
    return r
#جریمه تأخیر در ارسال لیست بیمه
def delaySendingList(right_insurance):
    return right_insurance * 0.2

#جریمه عدم پرداخت حق بیمه
def delayPayment(right_insurance,monthdelay):
    return right_insurance * monthdelay * 0.02 *monthdelay

#سهم بیمه‌شده از هزینه درمان
def Insured_share(treatment_cost,insured_share,peyment_ceiling):
    r = treatment_cost * insured_share
    if r >= peyment_ceiling:
        r = peyment_ceiling
    return r
#پاداش پایان خدمت
def termination_bonus(lastmonthsalary,yearsofWork):
    return lastmonthsalary * yearsofWork




