
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ['Button']
from .FormControl import FormControl

class Button(FormControl):
    inputType = 'button'
    submit = False

    def __init__(self, name=None, caption='', **kwd):
        if not caption:
            caption = 'Submit'
        FormControl.__init__(self, name, caption, **kwd)


    def propResources(self):
        return FormControl.propResources(self) + ['js_onclick']
        
    def preRender(self):
        if self.submit:
            self.inputType = 'submit'
    
    def drawValueAttr(self):
        if not self.value:
            self.value = self.defaultValue
        value = self.value or self._caption
        return "value='%s'" % self.htmlEncode(value)
        
