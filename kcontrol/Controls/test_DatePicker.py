import datetime
import unittest

from .DatePicker import DatePicker

class DatePickerTestCase(unittest.TestCase):

    def testDatePicker(self):
        # Basic value test
        ctrl = DatePicker('start_date')
        ctrl.showCalendar = False
        self.assertEqual(str(ctrl),
            """<input type='text' value='' id='start_date' name='start_date' onchange='handle_date_blur(this, "yyyy-MM-dd")' />""")

    def testFormat(self):
        ctrl = DatePicker('start_date')
        ctrl.mode = 'VIEW'
        val = datetime.datetime.now()
        res = val.strftime(ctrl.format)
        ctrl.value = val
        self.assertEqual(str(ctrl), str(res))

    def testDatePickerSpinner(self):
        # Basic value test
        ctrl = DatePicker('start_date')
        ctrl.showCalendar = False
        ctrl.showSpinner = True
        self.assertEqual(str(ctrl),
            """<input type='text' value='' id='start_date' name='start_date' onchange='handle_date_blur(this, "yyyy-MM-dd")' />
            <table cellpadding='0' cellspacing='0' border='0' style='display:inline;vertical-align:bottom;'>
            <tr>
                <td><a href='javascript:spinner_up("start_date")'><img src='/kcontrol/DatePicker/images/spinner_up.gif' border='0' /></a></td>
            </tr>
            <tr>
                <td><a href='javascript:spinner_down("start_date")'><img src='/kcontrol/DatePicker/images/spinner_down.gif' border='0' /></a></td>
            </tr>
            </table>
""")

    def testDatePickerCalendar(self):
        # Basic value test
        ctrl = DatePicker('start_date')

        self.assertEqual(str(ctrl), """                <table cellpadding='0' cellspacing='0' border='0'>
                <tr>
                    <td><input type='text' value='' id='start_date' name='start_date' onchange='handle_date_blur(this, "yyyy-MM-dd")' /></td>
                    <td><img src="/kcontrol/DatePicker/images/cal.gif" id="trigstart_date"
                        style="cursor: pointer; border: 1px solid red;"
                        onmouseover="this.style.background='red';"
                        onmouseout="this.style.background=''" align="middle" />
                <script type="text/javascript">
                    Calendar.setup({
                        inputField     : 'start_date',  // id of the input field
                        ifFormat    : '%Y-%m-%d',
                        showsTime    : false,    // will display a time selector
                        button        : 'trigstart_date',  // trigger for the calendar (button ID)
                        singleClick    : true,
                        step        : 1
                    });
                </script>
                    </td>
                  </tr>
                  </table>""")


if __name__ == '__main__':
    unittest.main()
