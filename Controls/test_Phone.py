
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
from kcontrol import ResWatcher
from kcontrol import Phone
import kcontrol.config as cfg


class PhoneTestCase(unittest.TestCase):
    def testPhone(self):
        # Basic value test
        ctrl = Phone('phone')
        self.assertEquals(str(ctrl),
            """<input type='text' value='' id='phone' name='phone' onblur='setPhone("phone")' />""")

    def testPhoneRes(self):
        # until we solve the threading problem
        return
        ctrl = Phone('phone')
        self.assertEquals(ResWatcher.js, ['Phone/js/phone_control.js'])

if __name__ == '__main__':
    unittest.main()
