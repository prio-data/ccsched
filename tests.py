
import datetime
import unittest

from ccsched import span 

class PartitioningTest(unittest.TestCase):
    def test_span(self):
        cases = [
            ("1999-01-01",1,3),
            ("2001-03-01",1,3),
            ("2020-04-01",4,6),
            ("1953-07-01",7,9),
            ("2071-11-01",10,12),
        ]

        for date,startMonth,endMonth in cases:
            start,end = span(datetime.date.fromisoformat(date),4)
            self.assertEqual(start.month,startMonth)
            self.assertEqual(end.month,endMonth)

        start,end = span(datetime.date(year=1999,month=4,day=1),2)
        self.assertEqual(start.month,1)
        self.assertEqual(end.month,6)

    def test_shift(self):
        cases = [
            ("2000-01-01",-1,10,12),
            ("1989-01-01",2,7,9),
            ("1992-01-01",4,1,3),
        ]

        for date,shift,startMonth,endMonth in cases:
            start,end = span(datetime.date.fromisoformat(date),4,shift=shift)
            self.assertEqual(start.month,startMonth)
            self.assertEqual(end.month,endMonth)

    def test_res(self):
        def fails():
            span(datetime.date(year=2002,month=1,day=1),7)
        self.assertRaises(ValueError,fails)

        cases = [
            ("1999-01-01",12,1,1),
            ("1999-03-01",6,3,4),
            ("2010-07-01",4,7,9),
        ]

        for date,res,startMonth,endMonth in cases:
            start,end = span(datetime.date.fromisoformat(date),res)
            self.assertEqual(start.month,startMonth)
            self.assertEqual(end.month,endMonth)

    def test_nooverlap(self):
        base = datetime.date.fromisoformat("1999-01-01")
        _,ea = span(base,4,shift=0)
        sb,_ = span(base,4,shift=1)
        self.assertNotEqual(ea,sb)

        sc = datetime.date.fromisoformat("1999-04-01")
        self.assertNotEqual(ea,sc)
