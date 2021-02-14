
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ['CheckBox']
from .FormControl import FormControl
from kcontrol import util

class CheckBox(FormControl):
    inputType = 'checkbox'

    def draw(self):
        # fix for cheetah useage
        if not self.value:
            self.value = self.defaultValue

        if util.str2bool(self.value):
            value = " checked='checked' "
        else:
            value = ''
        return """<input type='%s' 
    name='%s' 
    %s
    %s 
    %s>""" % (
            self.inputType,
            self.name,
            value,
            self.drawHtmlAttrs(),
            self.drawJSEvents()
        )
    @property
    def VIEW(self):
        if not self.value:
            return
        if str(self.value).upper() in ['1','YES','TRUE','ON','CHECKED']:
            return "<span style='color: #006600; font-weight: bold;'>Yes</span>"
        else:
            return "<span style='color: #990000; font-weight: bold;'>No</span>"
