from datetime import date
from unittest import TestCase
from ccsched import get_frac,get_month_frac
from ccsched import span_from_date as span

class PartitioningTest(TestCase):
    def test_span(self):
        cases = [
            ("1999-01-01",1,3),
            ("2001-03-01",1,3),
            ("2020-04-01",4,6),
            ("1953-07-01",7,9),
            ("2071-11-01",10,12),
        ]

        for dt,startMonth,endMonth in cases:
            start,end = span(date.fromisoformat(dt),4)
            self.assertEqual(start.month,startMonth)
            self.assertEqual(end.month,endMonth)

        start,end = span(date(year=1999,month=4,day=1),2)
        self.assertEqual(start.month,1)
        self.assertEqual(end.month,6)

    def test_shift(self):
        cases = [
            ("2000-01-01",-1,10,12),
            ("1989-01-01",2,7,9),
            ("1992-01-01",4,1,3),
        ]

        for dt,shift,startMonth,endMonth in cases:
            start,end = span(date.fromisoformat(dt),4,shift=shift)
            self.assertEqual(start.month,startMonth)
            self.assertEqual(end.month,endMonth)

    def test_res(self):
        def fails():
            span(date(year=2002,month=1,day=1),7)
        self.assertRaises(ValueError,fails)

        cases = [
            ("1999-01-01",12,1,1),
            ("1999-03-01",6,3,4),
            ("2010-07-01",4,7,9),
        ]

        for dt,res,startMonth,endMonth in cases:
            start,end = span(date.fromisoformat(dt),res)
            self.assertEqual(start.month,startMonth)
            self.assertEqual(end.month,endMonth)

    def test_nooverlap(self):
        base = date.fromisoformat("1999-01-01")
        _,ea = span(base,4,shift=0)
        sb,_ = span(base,4,shift=1)
        self.assertNotEqual(ea,sb)

        sc = date.fromisoformat("1999-04-01")
        self.assertNotEqual(ea,sc)

    def test_frac(self):
        args_results = [
            ((1,12,4,0),(1,3)),
            ((1,12,2,0),(1,6)),
            ((1,12,2,1),(7,12)),
            ((4,6,3,0),(4,4)),
            ((7,12,2,0),(7,9)),
            ((7,12,2,1),(10,12)),
            ((1,4,2,0),(1,2)),
            ((1,36,2,0),(1,18)),
            ((1,12,2,2),(13,18)),
        ]
        for args,result in args_results:
            self.assertEqual(get_frac(*args),result)

        fail_args = [
            (4,6,2,0)
        ]
        for args in fail_args:
            def fails():
                get_frac(*args)
            self.assertRaises(ValueError,fails)

    def test_date_frac(self):
        args_results = [
            (("1999-01-01","1999-12-01",2,0),("1999-01-01","1999-06-30")),
            (("1999-07-01","1999-12-01",2,0),("1999-07-01","1999-09-30")),
            (("1999-01-01","1999-12-01",6,1),("1999-03-01","1999-04-30")),
            (("1999-01-01","2000-02-01",2,0),("1999-01-01","1999-07-31")),
            (("1999-01-01","1999-12-01",2,2),("2000-01-01","2000-06-30")),
        ]
        for args,result in args_results:
            start,end,*args = args
            start,end = (date.fromisoformat(dt) for dt in (start,end))
            self.assertEqual(result,tuple((str(r) for r in get_month_frac(start,end,*args))))
