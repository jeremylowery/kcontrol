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

import unittest

from kcontrol import Link
import kcontrol.config as cfg


class LinkTestCase(unittest.TestCase):
    def testLinkValue(self):
        # Basic value test
        ctrl = Link('client_id')
        ctrl.value = 5
        self.assertEquals(str(ctrl),'5')

    def testLink(self):
        # Basic Link Test
        ctrl = Link('client_id')
        ctrl.value = 'John Smith'
        ctrl.link = '/clients/5'
        self.assertEquals(str(ctrl),"<a href='/clients/5'>John Smith</a>")

    def testLinkTarget(self):
        # Basic Link Test
        ctrl = Link('client_id')
        ctrl.target = '_blank'
        ctrl.value = 'John Smith'
        ctrl.link = '/clients/5'
        self.assertEquals(str(ctrl),"<a href='/clients/5' target='_blank'>John Smith</a>")


if __name__ == '__main__':
    unittest.main()
