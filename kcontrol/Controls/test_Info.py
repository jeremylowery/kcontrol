import unittest

from .Info import Info

class InfoTestCase(unittest.TestCase):
    def testInfo(self):
        # Basic value test
        ctrl = Info('client_id')
        ctrl.value = 5
        self.assertEqual(str(ctrl),
            "5")

if __name__ == '__main__':
    unittest.main()
