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

from kcontrol import Icon
import kcontrol.config as cfg


class IconTestCase(unittest.TestCase):
    def testIcon(self):
        # Basic value test
        ctrl = Icon('graphics/home.gif')
        ctrl.link = 'index.html'
        self.assertEquals(str(ctrl),
            "<a href='index.html' border='0'><img src='graphics/home.gif' " + 
            "alt='' title='' href='index.html' border='0'  /></a>")



if __name__ == '__main__':
    unittest.main()
