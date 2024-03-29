from typing import Tuple

import os
import math
from datetime import date

from dateutil.relativedelta import relativedelta
import fastapi
from fastapi.responses import JSONResponse

app = fastapi.FastAPI()

FRAC_SIZE = int(os.getenv("FRACTIONSIZE","4"))
if 12 % FRAC_SIZE != 0:
    raise ValueError("12 must be divisible by frac. size")

def get_frac(a: int, b:int, frac: int, shift: int)->Tuple[int,int]:
    """
    Get the fraction {shift} between numbers {a} and {b} given the divisor {frac}
    """
    try:
        assert a<=b 
    except AssertionError as e:
        raise ValueError("b must be bigger than a: "
                f"{a} !< {b}"
                ) from e

    span = (b-a) + 1

    try:
        assert span % frac == 0
    except AssertionError as e:
        raise ValueError(" span must be divisible by fraction: "
                f"{span} !% {frac}"
                ) from e

    unit = span / frac
    start = a + (unit*shift) 
    end = (a + (unit*(shift+1)))-1

    return int(start),int(end)

def get_month_frac(a,b,frac,shift):
    """
    Get the boundary dates for fraction {shift} in the span between dates 
    {a} and {b} given divisor {frac}
    """
    a = a.replace(day=1)
    b = b.replace(day=1)

    rel_b = relativedelta(b,a)
    rel_b_months = rel_b.months + (rel_b.years * 12)
    start,end = get_frac(a.month,a.month+rel_b_months,frac,shift)
    start_date = a + relativedelta(months=start-a.month)
    #start_date = a.replace(month=start)

    end_date = start_date + relativedelta(months=(end-start)+1)
    end_date = end_date - relativedelta(days=1)

    return start_date,end_date

def year_frac(year:int,frac:int,shift:int):
    """
    Get the boundary dates of fraction {shift} within year {year} given divisor {frac}
    """
    start = date(year=year,month=1,day=1)
    end = date(year=year,month=12,day=31)
    return get_month_frac(start,end,frac,shift)

def span_from_date(date_in:date, frac: int, shift:int=0):
    """
    Get the fraction span of the fraction containing {date_in}
    """
    try:
        assert 12 % frac == 0
    except AssertionError as e:
        raise ValueError("12 must be divisible by fraction size") from e
    unit = int(12/frac)
    current_frac = (math.ceil(date_in.month/(unit))-1)
    return get_month_frac(
            date(year=date_in.year,month=1,day=1),
            date(year=date_in.year,month=12,day=31),
            frac = frac,
            shift = current_frac+shift)

def span_as_response(start,end):
    """
    Format start and end dates as a JSON response
    """
    rd = relativedelta(end,start)
    duration = (rd.months + (rd.years * 12))+1
    return {
        "start": start,
        "end": end,
        "duration_months": duration 
    }

@app.get("/{start}/{end}/{frac}/{shift}/")
def serve_month_frac(start:date,end:date,frac:int,shift:int):
    try:
        f_start,f_end = get_month_frac(start,end,frac,shift)
    except ValueError as e:
        return JSONResponse({"error":str(e)},status_code=400)
    return span_as_response(f_start,f_end)

@app.get("/{year}/{shift}")
def handle_year_fraction(year:int,shift:int,fraction:int=None):
    """
    Get fraction {shift} in year {year} given divisor {fraction}
    """
    if fraction is None:
        fraction = FRAC_SIZE
    return span_as_response(*year_frac(year,fraction,shift))

@app.get("/today/{frac}/{shift}/")
def span_from_today(frac:int,shift:int):
    """
    Get the current fraction span 
    """
    today = date.today()
    try:
        f_start,f_end = span_from_date(today,frac,shift)
    except ValueError as e:
        return JSONResponse({"error":str(e)},status_code=400)
    return span_as_response(f_start,f_end)

@app.get("/")
def quarter_span(shift:int=0):
    return span_from_today(frac = FRAC_SIZE, shift = shift)
