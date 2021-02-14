import unittest

from .TextBox import TextBox

class TextBoxTestCase(unittest.TestCase):
    def testTextBox(self):
        # Basic value test
        ctrl = TextBox('first_name')
        ctrl.value ="'#' - '$' Yoda"
        self.assertEqual(str(ctrl), 
            "<input type='text' value='&apos;#&apos; - &apos;$&apos; Yoda' id='first_name' name='first_name'  />")

    def testPasswordMask(self):
        ctrl = TextBox('password')
        ctrl.mask=1
        self.assertEqual(str(ctrl), 
            "<input type='password' value='' id='password' name='password'  />")

if __name__ == '__main__':
    unittest.main()
