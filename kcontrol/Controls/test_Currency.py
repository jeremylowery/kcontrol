
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.


import unittest
import math

from .Currency import Currency

class CurrencyTestCase(unittest.TestCase):
    def testCurrency(self):
        # Basic value test
        ctrl = Currency('total')
        self.assertEqual(str(ctrl),
            """<input type='text' value='' style='text-align:right;' id='total' name='total' onchange='formatCurrency("total",1);' />""")


    def testCurrencySign(self):
        # Basic value test
        ctrl = Currency('total')
        ctrl.hideSign = True
        self.assertEqual(str(ctrl),
            """<input type='text' value='' style='text-align:right;' id='total' name='total' onchange='formatCurrency("total",0);' />""")

        ctrl.hideSign = False
        self.assertEqual(ctrl.view, '')
        ctrl.value = math.pi
        self.assertEqual(ctrl.view, '$3.14')
    
        ctrl.value = 3
        self.assertEqual(ctrl.view, '$3.00')
        
        ctrl.value = -1.223
        self.assertEqual(ctrl.view,
            "<span style='color:#FF0000;'>$1.22</span>")


if __name__ == '__main__':
    unittest.main()
