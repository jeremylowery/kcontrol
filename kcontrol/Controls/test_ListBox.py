import unittest

from .ListBox import ListBox

class ListBoxTestCase(unittest.TestCase):
    def testListBox(self):
        # Basic value test
        ctrl = ListBox('client_id','Client ID')
        ctrl.addValue('f','Female')
        ctrl.addValue('m','Male')
        self.assertEqual(str(ctrl),
            """<select size='1' id='client_id' name='client_id' >
<option value='f' >Female</option>
<option value='m' >Male</option>
</select>
""")


if __name__ == '__main__':
    unittest.main()
