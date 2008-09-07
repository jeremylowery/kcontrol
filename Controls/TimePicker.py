
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ['TimePicker']
import datetime
from kcontrol.Controls.TextBox import *
from kcontrol.url import res

class TimePicker(TextBox):
    defaultNow = False
    validate = True
    showAMorPM = True

    def _get_defaultValue(self):
        now = datetime.datetime.now()
        if self.defaultNow:
            if self.showAMorPM:
                return "%i:%s %s" % (int(now.strftime("%I")),
                                         now.strftime("%M"),
                                         now.strftime("%p"))
            else:
                return "%i:%s" % (int(now.strftime("%I")),
                                      now.strftime("%M"))
        else:
            return self._defaultValue
    defaultValue = property(_get_defaultValue, TextBox._set_defaultValue, doc=TextBox._doc_defaultValue)

    def buildResources(self):
        self.pushResourceUp('js', res('TimePicker/js/timepicker.js'))
        self.addJSEvent('onkeydown', '{time_help(this, event); if(event.ctrlKey == true) return false;}\n')
        self.addJSEvent('onblur', 'handle_time_blur(this)')
        self.addHtmlAttr('size', '8')
        self.addHtmlAttr('style','text-align: right;')
        TextBox.buildResources(self)

    def draw(self):
        buf = TextBox.draw(self)
        if self.validate:
            buf = buf + """
    <script type="text/javascript">
        handle_time_blur(getObj('%(name)s'));
    </script>
""" % dict(name=self.name)
        return buf

    @property
    def VIEW(self):
        if not self.value:
            return ''
        if isinstance(self.value, str):
            return self.value
        if self.showAMorPM:
            return self.value.strftime("%I:%M %p")
        return self.value.strftime("%I:%M")
