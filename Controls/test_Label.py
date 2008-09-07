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

from kcontrol import Label
import kcontrol.config as cfg


class LabelTestCase(unittest.TestCase):
    def testLabel(self):
        # Basic value test
        ctrl = Label('client_id','Client ID')
        self.assertEquals(str(ctrl),
            "<label for='client_id'>Client ID</label>")



if __name__ == '__main__':
    unittest.main()
