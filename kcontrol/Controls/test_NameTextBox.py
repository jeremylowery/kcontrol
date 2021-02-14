import unittest

from .NameTextBox import NameTextBox

class NameTextBoxTestCase(unittest.TestCase):
    def testNameTextBox(self):
        # Basic value test
        ctrl = NameTextBox('client_name')
        self.assertEqual(str(ctrl),
            """
<input type='hidden' value='' id='title_name' name='title_name'  />
<input type='hidden' value='' id='first_name' name='first_name'  />
<input type='hidden' value='' id='middle_name' name='middle_name'  />
<input type='hidden' value='' id='last_name' name='last_name'  />
<input type='hidden' value='' id='suffix_name' name='suffix_name'  />

                  <input type='text' name='client_name' id='client_name' id='client_name' name='client_name' onchange='this.name_ctrl.elemSync()' value='' />
            <script language='Javascript'>
                (new NameCtrl('client_name', '%T %F %M %L %S', 'title_name', 
                    'first_name', 'middle_name', 'last_name', 'suffix_name')
                  ).hiddenToElem()
            </script>
""")


if __name__ == '__main__':
    unittest.main()
