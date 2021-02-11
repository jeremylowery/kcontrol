###############################################################################
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license
# 
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.
###############################################################################

import sys
import math
import unittest

from kcontrol import Number
import kcontrol.config as cfg

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
        self.assertEquals(str(ctrl),
            """<input type='text' value='' style='text-align:right;' """ \
            """id='total' name='total' onblur='formatNumber("total", 2) ' />""")

    def testNumberDecimals(self):
        print(count())
        # Basic value test
        ctrl = Number('total')
        ctrl.decimals = 4
        self.assertEquals(str(ctrl),
            """<input type='text' value='' style='text-align:right;' """ \
            """id='total' name='total' onblur='formatNumber("total", 4) ' />""")
    
    def testNumberView(self):
        print(count())
        ctrl = Number('total')
        ctrl.decimals = 4
        self.assertEquals(ctrl.view, '')
        ctrl.value = math.pi
        self.assertEquals(ctrl.view, '3.1416')

        ctrl.decimals = 0
        self.assertEquals(ctrl.view, '3')
        
        ctrl.decimals = 3
        self.assertEquals(ctrl.view, '3.142')

        ctrl.value = -1.223
        self.assertEquals(ctrl.view,
            "<span style='color:#FF0000;'>-1.22</span>")

        ctrl.value = ''
        self.assertEquals(ctrl.view, '')

    def testNumberMode(self):
        print(count())
        ctrl = Number('total')
        ctrl.decimals = 4
        ctrl.mode = 'VIEW'
        self.assertEquals(str(ctrl), '4.0000')

if __name__ == '__main__':
    unittest.main()
