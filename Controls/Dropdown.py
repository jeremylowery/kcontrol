
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ['TextBox']

import cStringIO

from FormControl import FormControl

class Dropdown(FormControl):
    inputType = 'text'
    
    def __init__(self, *a, **k):
        self.options = []
        FormControl.__init__(self, *a, **k)

    def preRender(self):
        FormControl.preRender(self)
    
    def draw(self):
        buf = cStringIO.StringIO()
        buf.write("<select %s %s>" % (
            self.drawHtmlAttrs(),
            self.drawJSEvents()))
        for value, label in self.options:
            if value == self.value:
                buf.write("<option value='%s' selected='selected'>%s</option>" % (value, label))
            else:
                buf.write("<option value='%s'>%s</option>" % (value, label))
        buf.write("</select>")
        buf.seek(0)
        return buf.getvalue()

    def add_option(self, value, label=None):
        if label is None:
            label = value
        self.options.append((value, label))

    def __draw(self):
        # fix for cheetah useage
        if not self.value:
            self.value = self.defaultValue
            
        if self.size == 1:
            return FormControl.draw(self)
        if self.mask:
            raise SystemError, "A control cannot have a size greater than one and a mask property of True"
        
        if self.value:
            value = self.value
        else:
            value = ''
        return "<textarea name='%s' id='%s' rows='%s' %s %s>%s</textarea>" % (
            self.name,
            self.htmlID,
            self.size,
            self.drawHtmlAttrs(),
            self.drawJSEvents(),
            value
        )
