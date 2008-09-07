"""
    Formats > 10 digit : (xxx) xxx-xxxx ext: x2
    Formats 10 digit   : (xxx) xxx-xxxx
    Fomats 7 diget     : xxx-xxxx   
    Igores everything else
"""

# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.


__all__ = ['Phone']
from kcontrol.Controls.TextBox import TextBox
from kcontrol.url import res

class Phone(TextBox):
    inputType = 'text'
    size = 1
    mask = False

    def buildResources(self):
        self.pushResourceUp('js',res('Phone/js/phone_control.js'))
        self.addJSEvent("onblur", 'setPhone("%s")' % self.name)
        TextBox.buildResources(self)

    def draw(self):
        return "%s\n%s" % (TextBox.draw(self),
            "<script type='text/javascript'>setPhone('%s')</script>" % \
            self.name)
