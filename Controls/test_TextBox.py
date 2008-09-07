
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

from kcontrol import TextBox
import kcontrol.config as cfg


class TextBoxTestCase(unittest.TestCase):
    def testTextBox(self):
        # Basic value test
        ctrl = TextBox('first_name')
        ctrl.value ="'#' - '$' Yoda"
        self.assertEquals(str(ctrl), 
            "<input type='text' value='&apos;#&apos; - &apos;$&apos; Yoda' id='first_name' name='first_name'  />")

        #print 'ctrl', ctrl
        #print 'html', ctrl.html
        #print 'form', ctrl.form
        #print 'view', ctrl.view
        #print 'base', ctrl.base

    def testPasswordMask(self):
        ctrl = TextBox('password')
        ctrl.mask=1
        self.assertEquals(str(ctrl), 
            "<input type='password' value='' id='password' name='password'  />")

if __name__ == '__main__':
    unittest.main()
