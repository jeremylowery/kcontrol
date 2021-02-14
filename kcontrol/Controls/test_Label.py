import unittest

from .Label import Label

class LabelTestCase(unittest.TestCase):
    def testLabel(self):
        # Basic value test
        ctrl = Label('client_id','Client ID')
        self.assertEqual(str(ctrl),
            "<label for='client_id'>Client ID</label>")

if __name__ == '__main__':
    unittest.main()
