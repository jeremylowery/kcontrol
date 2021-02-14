import unittest

from .Icon import Icon

class IconTestCase(unittest.TestCase):
    def testIcon(self):
        # Basic value test
        ctrl = Icon('graphics/home.gif')
        ctrl.link = 'index.html'
        self.assertEqual(str(ctrl),
            "<a href='index.html' border='0'><img src='graphics/home.gif' " + 
            "alt='' title='' href='index.html' border='0'  /></a>")

if __name__ == '__main__':
    unittest.main()
