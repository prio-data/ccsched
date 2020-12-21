
import os
import math
import datetime

import datetime
from dateutil.relativedelta import relativedelta

from dataclasses import dataclass

import fastapi
from fastapi import Request
from fastapi.responses import JSONResponse

fractionSize = int(os.getenv("FRACTIONSIZE",4))
if 12 % fractionSize != 0:
    raise ValueError("12 must be divisible by fraction size!")

app = fastapi.FastAPI()

def span(date:datetime.date,frac:int,shift=0):
    if 12 % frac != 0:
        raise ValueError("12 must be divisible by month fraction")
    fracsize = int(12 / frac)

    if shift != 0:
        date = date + relativedelta(months=shift*fracsize)

    currentFrac = math.ceil(date.month/(fracsize))
    startmonth = ((currentFrac-1)*fracsize) + 1
    start = datetime.date(year=date.year,month=startmonth,day=1)
    end = (start + relativedelta(months=fracsize))-datetime.timedelta(days=1)

    return start,end
 
@app.get("/")
def main(req: Request, shift: int = 0):
    start,end = span(datetime.date.today(),fractionSize,shift=shift)
    return JSONResponse({"start":str(start),"end":str(end)}) 
