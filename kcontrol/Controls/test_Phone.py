import unittest
from kcontrol import ResWatcher
from .Phone import Phone

class PhoneTestCase(unittest.TestCase):
    def testPhone(self):
        # Basic value test
        ctrl = Phone('phone')
        self.assertEqual(str(ctrl),
            """<input type='text' value='' id='phone' name='phone' onblur='setPhone("phone")' />""")

    def testPhoneRes(self):
        # until we solve the threading problem
        return
        ctrl = Phone('phone')
        self.assertEqual(ResWatcher.js, ['Phone/js/phone_control.js'])

if __name__ == '__main__':
    unittest.main()
