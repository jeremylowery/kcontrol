import unittest

from kcontrol import Bullet
from kcontrol import Link

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
        self.assertEqual(str(ctrl),
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
        self.assertEqual(str(ctrl),
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
        self.assertEqual(str(ctrl),
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

