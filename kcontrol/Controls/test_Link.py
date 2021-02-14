import unittest

from .Link import Link

class LinkTestCase(unittest.TestCase):
    def testLinkValue(self):
        # Basic value test
        ctrl = Link('client_id')
        ctrl.value = 5
        self.assertEqual(str(ctrl),'5')

    def testLink(self):
        # Basic Link Test
        ctrl = Link('client_id')
        ctrl.value = 'John Smith'
        ctrl.link = '/clients/5'
        self.assertEqual(str(ctrl),"<a href='/clients/5'>John Smith</a>")

    def testLinkTarget(self):
        # Basic Link Test
        ctrl = Link('client_id')
        ctrl.target = '_blank'
        ctrl.value = 'John Smith'
        ctrl.link = '/clients/5'
        self.assertEqual(str(ctrl),"<a href='/clients/5' target='_blank'>John Smith</a>")

if __name__ == '__main__':
    unittest.main()
