
from past.builtins import basestring
__all__ = ['DatePicker']
import datetime
from .TextBox import TextBox

class DatePicker(TextBox):
    defaultToday = False
    showSpinner = False
    showCalendar = True
    showTime = False

    validate = True

    dateFormat = '%m/%d/%Y'
    dateFormat2 = 'MM/dd/yyyy'

    timeFormat = '%I:%M %p'
    timeFormat2 = 'hh:mm a'

    @property
    def format(self):
        if self.showTime:
            return "%s %s" % (self.dateFormat, self.timeFormat)
        else:
            return self.dateFormat

    @property
    def format2(self):
        if self.showTime:
            return "%s %s" % (self.dateFormat2, self.timeFormat2)
        else:
            return self.dateFormat2
    
    def _get_defaultValue(self):
        if self.defaultToday:
            return datetime.datetime.now().strftime(self.format)
        else:
            return self._defaultValue
    defaultValue = property(_get_defaultValue,
                            TextBox._set_defaultValue,
                            doc=TextBox._doc_defaultValue)

    def buildResources(self):
        self.pushResourceUp('css', 'calendar.css')
        self.pushResourceUp('js', 'calendar.js')
        self.pushResourceUp('js', 'calendar-en.js')
        self.pushResourceUp('js', 'calendar-setup.js')
        change = "handle_date_blur(this, '%s')" % self.format2
        self.addJSEvent('onchange', change)
        TextBox.buildResources(self)

    def draw(self):
        img_path = '/repo/img/kcontrol'

        if not self.value or isinstance(self.value, basestring):
            pass
        else:
            try:
                self.value = self.value.strftime(self.format)
            except ValueError:
                pass

        buf = TextBox.draw(self)
        if self.showSpinner:
            buf = buf + """
            <table cellpadding='0' cellspacing='0' border='0'
                   style='display:inline;vertical-align:bottom;'>
            <tr>
                <td><a href='javascript:spinner_up("%s")'><img
                       src='%s/spinner_up.gif' border='0' /></a></td>
            </tr>
            <tr>
                <td><a href='javascript:spinner_down("%s")'><img
                       src='%s/spinner_down.gif' border='0' /></a></td>
            </tr>
            </table>
            """ % (self.name, img_path, self.name, img_path)

        if self.showTime:
            st = 'true'
        else:
            st = 'false'

        id = self.htmlAttrs.get('id', self.name)
        if self.showCalendar:
            buf = """\
                <table cellpadding='0' cellspacing='0' border='0'>
                <tr>
                    <td>%s</td>
                    <td><img src="%s/cal.gif" id="trig%s"
                        style="cursor: pointer; border: 1px solid red;"
                        onmouseover="this.style.background='red';"
                        onmouseout="this.style.background=''" align="middle" />
                <script type="text/javascript">
                    Calendar.setup({
                        inputField     : '%s',  // id of the input field
                        ifFormat    : '%s',
                        showsTime    : %s,    // will display a time selector
                        // trigger for the calendar (button ID)
                        button        : 'trig%s',  
                        singleClick    : true,
                        step        : 1
                    });
                </script>
                    </td>
                  </tr>
                  </table>""" % (buf, img_path, id,
                                    id, self.format, st,
                                   id)
        return buf

    @property
    def VIEW(self):
        if not self.value:
            return ''
        if isinstance(self.value, str):
            return self.value
        return self.value.strftime(self.format)

