import unittest

from .Hidden import Hidden

class HiddenTestCase(unittest.TestCase):
    def testHidden(self):
        # Basic value test
        ctrl = Hidden('client_id')
        ctrl.value = 5
        self.assertEqual(str(ctrl),
            "<input type='hidden' value='5' id='client_id' name='client_id'  />")

if __name__ == '__main__':
    unittest.main()
