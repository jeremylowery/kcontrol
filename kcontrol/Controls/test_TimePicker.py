import datetime
import unittest

from datetime import datetime
from .TimePicker import TimePicker

class TimePickerTestCase(unittest.TestCase):
    def testTimePicker(self):
        # Basic value test
        ctrl = TimePicker('appointment_time')
        ctrl.defaultNow = True
        ctrl.showAMorPM = False
        time = "%i:%s" % (int(datetime.now().strftime("%I")), datetime.now().strftime("%M"))

        self.assertEqual(str(ctrl),
            """<input type='text' value='%s' id='appointment_time' name='appointment_time' onblur='handle_time_blur(this)' onkeydown='{time_help(this, event); if(event.ctrlKey == true) return false;}' />
    <script type="text/javascript">
        handle_time_blur(document.getElementByID('appointment_time'));
    </script>
""" % time)

    def testTimePickerAMPM(self):
        # Basic value test
        ctrl = TimePicker('appointment_time')
        ctrl.defaultNow = True
        time = "%i:%s %s" % (int(datetime.now().strftime("%I")), datetime.now().strftime("%M"), datetime.now().strftime("%p"))
        self.assertEqual(str(ctrl),
            """<input type='text' value='%s' id='appointment_time' name='appointment_time' onblur='handle_time_blur(this)' onkeydown='{time_help(this, event); if(event.ctrlKey == true) return false;}' />
    <script type="text/javascript">
        handle_time_blur(document.getElementByID('appointment_time'));
    </script>
""" % time)

if __name__ == '__main__':
    unittest.main()
