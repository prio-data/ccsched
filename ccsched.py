from typing import Tuple

import os
import math
import datetime
from datetime import date

from dateutil.relativedelta import relativedelta

from dataclasses import dataclass

import fastapi
from fastapi import Request
from fastapi.responses import JSONResponse,Response

app = fastapi.FastAPI()

def get_frac(a: int, b:int, frac: int, shift: int)->Tuple[int,int]:
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

def span_from_date(date_in:date, frac: int, shift:int=0):
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

@app.get("/{start}/{end}/{frac}/{shift}/")
def serve_month_frac(start:date,end:date,frac:int,shift:int):
    try:
        f_start,f_end = get_month_frac(start,end,frac,shift)
    except ValueError as e:
        return JSONResponse({"error":str(e)},status_code=400)
    return JSONResponse({"start":str(f_start),"end":str(f_end)})

@app.get("/today/{frac}/{shift}/")
def span_from_today(frac:int,shift:int):
    today = date.today()
    try:
        f_start,f_end = span_from_date(today,frac,shift)
    except ValueError as e:
        return JSONResponse({"error":str(e)},status_code=400)
    return JSONResponse({"start":str(f_start),"end":str(f_end)})
