
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.


__all__ = ['SSN']
from kcontrol.Controls.TextBox import TextBox

class SSN(TextBox):
    """   
        Formats 10 digit : 0-123-45-6789
        Formats 9 digit  : 123-45-6789
        Igores everything else
        
        OPTIONS
            :multi: True by default
                If multi is True:
                    Then three textboxes will
                    be displayed, the actuall value will 
                    be stored in a hidden element.
                If multi is False:
                    Then only one textbox will be displayed.
                    In this case a hidden element is not 
                    needed.
        *NOTE
            :multi: does not yet handle 10 digit ssn's.
                If multi is True:, only a 9 digit SSN will
                be created.
    """
    multi = True
    
    def draw(self):
        if self.multi:
            self.inputType = 'hidden'
            return self.multiDraw()
        else:
            self.inputType = 'text'
            return self.singleDraw()
            
    def multiDraw(self):
        buf = """
        <input
             type="text"
             name="%(name)s_1"
             id="%(name)s_1"
             size="2"
             onblur="SSNsyncToHidden('%(name)s')" />
        -
        <input 
            type="text" 
            name="%(name)s_2" 
            id="%(name)s_2" 
            size="2"
            onblur="SSNsyncToHidden('%(name)s')" />
        -
        <input 
            type="text" 
            name="%(name)s_3" 
            id="%(name)s_3" 
            size="3" 
            onblur="SSNsyncToHidden('%(name)s')"/>
            
        <SCRIPT TYPE="text/javascript">
        <!-- 
        // SSN Control Javascript
        autojump('%(name)s_1', '%(name)s_2', 3);
        autojump('%(name)s_2', '%(name)s_3', 2);
        SSNsyncFromHidden('%(name)s');
        //-->
        </SCRIPT>
""" % dict(name=self.name)
        return "\n".join([TextBox.draw(self), buf])
    
    def singleDraw(self):
        self.addJSEvent("onblur", 'setSSN("%s")' % self.name)
        return TextBox.draw(self)

    def buildResources(self):
        self.pushResourceUp('js','ssn_control.js')
        TextBox.buildResources(self)
