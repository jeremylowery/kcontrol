import unittest

from .Button import Button

class ButtonTestCase(unittest.TestCase):
    def testButton(self):
        # Basic value test
        ctrl = Button('add_form_button')
        ctrl.defaultValue = 'Foo'
        self.assertEqual(str(ctrl),
            "<input type='button' value='Submit' id='add_form_button' name='add_form_button'  />")

        ctrl = Button('foo')
        ctrl.submit = True
        self.assertEqual(str(ctrl),
            "<input type='submit' value='Submit' id='foo' name='foo'  />")

if __name__ == '__main__':
    unittest.main()
