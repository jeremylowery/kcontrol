###############################################################################
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license
# 
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.
###############################################################################

import unittest

from mx.DateTime import now
from kcontrol import TimePicker
import kcontrol.config as cfg
import datetime

class TimePickerTestCase(unittest.TestCase):
    def testTimePicker(self):
        # Basic value test
        ctrl = TimePicker('appointment_time')
        ctrl.defaultNow = True
        ctrl.showAMorPM = False
        time = "%i:%s" % (int(now().strftime("%I")), now().strftime("%M"))
     
        self.assertEquals(str(ctrl),
            """<input type='text' value='%s' id='appointment_time' name='appointment_time' onblur='handle_time_blur(this)' onkeydown='{time_help(this, event); if(event.ctrlKey == true) return false;}' />
    <script type="text/javascript">
        handle_time_blur(document.getElementByID('appointment_time'));
    </script>
""" % time)


    def testTimePickerAMPM(self):
        # Basic value test
        ctrl = TimePicker('appointment_time')
        ctrl.defaultNow = True
        time = "%i:%s %s" % (int(now().strftime("%I")), now().strftime("%M"), now().strftime("%p"))
        self.assertEquals(str(ctrl),
            """<input type='text' value='%s' id='appointment_time' name='appointment_time' onblur='handle_time_blur(this)' onkeydown='{time_help(this, event); if(event.ctrlKey == true) return false;}' />
    <script type="text/javascript">
        handle_time_blur(document.getElementByID('appointment_time'));
    </script>
""" % time)

if __name__ == '__main__':
    unittest.main()
