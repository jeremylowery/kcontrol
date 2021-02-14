import unittest

from .SSN import SSN
from kcontrol import ResWatcher

class SSNTestCase(unittest.TestCase):
    def testSSN(self):
        # Basic value test
        ctrl = SSN('ssn')
        self.assertEqual(str(ctrl),
            """<input type='hidden' value='' id='ssn' name='ssn'  />

        <input
             type="text"
             name="ssn_1"
             id="ssn_1"
             size="2"
             onblur="SSNsyncToHidden('ssn')" />
        -
        <input 
            type="text" 
            name="ssn_2" 
            id="ssn_2" 
            size="2"
            onblur="SSNsyncToHidden('ssn')" />
        -
        <input 
            type="text" 
            name="ssn_3" 
            id="ssn_3" 
            size="3" 
            onblur="SSNsyncToHidden('ssn')"/>
            
        <SCRIPT TYPE="text/javascript">
        <!-- 
        // SSN Control Javascript
        autojump('ssn_1', 'ssn_2', 3);
        autojump('ssn_2', 'ssn_3', 2);
        SSNsyncFromHidden();
        //-->
        </SCRIPT>
""")


    def testSSNSingle(self):
        # basic value test
        ctrl = SSN('ssn')
        ctrl.multi = False
        self.assertEqual(str(ctrl),
            """<input type='text' value='' id='ssn' name='ssn' onblur='setSSN("ssn")' />""")

    def testSSNRes(self):
        return
        # until we solve the threading problem
        ctrl = SSN('ssn')
        self.assertEqual(ResWatcher.js,['SSN/js/ssn_control.js'])

if __name__ == '__main__':
    unittest.main()
