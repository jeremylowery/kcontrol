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

from kcontrol import Bullet
from kcontrol import Link
import kcontrol.config as cfg


class BulletTestCase(unittest.TestCase):

    def testBullet(self):
        # Basic value test
        links = [
            ('google','http://www.google.com'),
            ('yahoo','http://www.yahoo.com'),
            ('koarcg','http://www.koarcg.com'),
        ]
        ctrl = Bullet('my_list')
        for link in links:
            li = Link(link[0])
            li.link = link[1]
            ctrl.addControl(li)
        self.assertEquals(str(ctrl),
            """<ul type='disc' >
    <li>
     <a href='http://www.google.com'></a>
    </li>
    <li>
     <a href='http://www.yahoo.com'></a>
    </li>
    <li>
     <a href='http://www.koarcg.com'></a>
    </li>
</ul>
""")

    def testBulletUL(self):
        # Basic value test
        links = [
            ('google','http://www.google.com'),
            ('yahoo','http://www.yahoo.com'),
            ('koarcg','http://www.koarcg.com'),
        ]
        ctrl = Bullet('my_list')
        ctrl.mode = 'square'
        for link in links:
            li = Link(link[0])
            li.link = link[1]
            ctrl.addControl(li)
        self.assertEquals(str(ctrl),
            """<ul type='square' >
    <li>
     <a href='http://www.google.com'></a>
    </li>
    <li>
     <a href='http://www.yahoo.com'></a>
    </li>
    <li>
     <a href='http://www.koarcg.com'></a>
    </li>
</ul>
""")

    def testBulletOL(self):
        # Basic value test
        links = [
            ('google','http://www.google.com'),
            ('yahoo','http://www.yahoo.com'),
            ('koarcg','http://www.koarcg.com'),
        ]
        ctrl = Bullet('my_list')
        ctrl.mode = 'number'
        for link in links:
            li = Link(link[0])
            li.link = link[1]
            ctrl.addControl(li)
        self.assertEquals(str(ctrl),
            """<ol type='1' >
    <li>
     <a href='http://www.google.com'></a>
    </li>
    <li>
     <a href='http://www.yahoo.com'></a>
    </li>
    <li>
     <a href='http://www.koarcg.com'></a>
    </li>
</ol>
""")

if __name__ == '__main__':
    unittest.main()

