
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.


import unittest

from kcontrol import SSN
from kcontrol import ResWatcher


class SSNTestCase(unittest.TestCase):
    def testSSN(self):
        # Basic value test
        ctrl = SSN('ssn')
        self.assertEquals(str(ctrl),
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
        self.assertEquals(str(ctrl),
            """<input type='text' value='' id='ssn' name='ssn' onblur='setSSN("ssn")' />""")

    def testSSNRes(self):
        return
        # until we solve the threading problem
        ctrl = SSN('ssn')
        self.assertEquals(ResWatcher.js,['SSN/js/ssn_control.js'])

if __name__ == '__main__':
    unittest.main()
