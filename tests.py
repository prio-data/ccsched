
from datetime import date
from unittest import TestCase
from ccsched import get_frac,get_month_frac

class TestSched(TestCase):
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

