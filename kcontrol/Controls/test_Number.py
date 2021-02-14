import sys
import math
import unittest

from .Number import Number

x = 0
def count():
    global x
    x = x + 1
    return x

class NumberTestCase(unittest.TestCase):
    def testNumber(self):
        print(count())
        # Basic value test
        ctrl = Number('total')
        self.assertEqual(str(ctrl),
            """<input type='text' value='' style='text-align:right;' """ \
            """id='total' name='total' onblur='formatNumber("total", 2) ' />""")

    def testNumberDecimals(self):
        print(count())
        # Basic value test
        ctrl = Number('total')
        ctrl.decimals = 4
        self.assertEqual(str(ctrl),
            """<input type='text' value='' style='text-align:right;' """ \
            """id='total' name='total' onblur='formatNumber("total", 4) ' />""")
    
    def testNumberView(self):
        print(count())
        ctrl = Number('total')
        ctrl.decimals = 4
        self.assertEqual(ctrl.view, '')
        ctrl.value = math.pi
        self.assertEqual(ctrl.view, '3.1416')

        ctrl.decimals = 0
        self.assertEqual(ctrl.view, '3')
        
        ctrl.decimals = 3
        self.assertEqual(ctrl.view, '3.142')

        ctrl.value = -1.223
        self.assertEqual(ctrl.view,
            "<span style='color:#FF0000;'>-1.22</span>")

        ctrl.value = ''
        self.assertEqual(ctrl.view, '')

    def testNumberMode(self):
        print(count())
        ctrl = Number('total')
        ctrl.decimals = 4
        ctrl.mode = 'VIEW'
        self.assertEqual(str(ctrl), '4.0000')

if __name__ == '__main__':
    unittest.main()
