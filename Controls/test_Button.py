
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

from kcontrol import Button
import kcontrol.config as cfg


class ButtonTestCase(unittest.TestCase):
    def testButton(self):
        # Basic value test
        ctrl = Button('add_form_button')
        ctrl.defaultValue = 'Foo'
        self.assertEquals(str(ctrl),
            "<input type='button' value='Submit' id='add_form_button' name='add_form_button'  />")

        ctrl = Button('foo')
        ctrl.submit = True
        self.assertEquals(str(ctrl),
            "<input type='submit' value='Submit' id='foo' name='foo'  />")

if __name__ == '__main__':
    unittest.main()
