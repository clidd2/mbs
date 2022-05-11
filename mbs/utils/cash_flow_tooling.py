import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta


def date_offset(start_date, month_offset):
    return start_date + relativedelta(months=month_offset)

def calc_payment_dates(start_date, end_date, periodicity=12) -> dict:
    '''
    given a start date, an end date, and periodity (number of payments per year)
    calculate payment dates for security. Will assume period between today and
    start date will be accrued.
    dt.date start_date: first payment date relative to now
    dt.date end_date: last payment date of security; effectively maturity date
    int periodity: number of payments per year. assumed to be 12 for mortgage
                   calculations
    return: dictionary of form {period : dt.date} containing all remaining
            periods and dates for security in question
    '''

    #some broad assertions - will look into how these are generally handled


    days = (end_date - start_date).days
    #VERY rough assumptions right now - looking for MVP vs perfection
    full_years = days // 365.25
    rem = days / 365.25 - full_years

    periods = int(full_years * periodicity)
    month_offset = int(12 / periodicity)
    return {period : date_offset(start_date, month_offset * period) for period in range(0, periods+1)}







def pretty_print_float(val):
    try:
        val = float(val)
        print(f'{val:,.2f}')

    except Exception as err:
        return -1
