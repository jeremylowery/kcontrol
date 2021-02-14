from kcontrol.Controls.Control import Control
from kcontrol.Controls.CompositeControl import CompositeControl
from kcontrol.Controls.FormControl import FormControl
from kcontrol.Controls.Hidden import *
from kcontrol.Controls.TextBox import *

class NameTextBox(FormControl, CompositeControl):
    titleName = 'title_name'
    firstName = 'first_name'
    middleName = 'middle_name'
    lastName = 'last_name'
    suffixName = 'suffix_name'
    _relpath = 'form/NameTextBox'
    format = '%T %F %M %L %S'

    def _get_caption(self):
        label = Label(caption=self._caption)
        label.ds = self.name
        return label.render()
    caption = property(_get_caption, CompositeControl._set_caption)

    def buildResources(self):
        CompositeControl.buildResources(self)
        self.pushResourceUp('js', 'name_ctrl.js')

    def buildControls(self):
        CompositeControl.buildControls(self)

        self.addControl(Hidden(self.titleName, ''))
        self.addControl(Hidden(self.firstName, ''))
        self.addControl(Hidden(self.middleName, ''))
        self.addControl(Hidden(self.lastName, ''))
        self.addControl(Hidden(self.suffixName, ''))

    def preRender(self):
        CompositeControl.preRender(self)
        self.addJSEvent(
            'onchange', "this.name_ctrl.elemSync()"
        )

    def draw(self):
        return """%(elems)s
                  %(control)s
            <script language='Javascript'>
                (new NameCtrl('%(name)s', '%(format)s', '%(title)s', 
                    '%(first)s', '%(middle)s', '%(last)s', '%(suffix)s')
                  ).hiddenToElem()
            </script>
""" % {
                'elems' : CompositeControl.draw(self),
                'control' : self.drawTextBox(),
                'format' : self.format,
                'name' : self.name,
                'title' : self.titleName,
                'first' : self.firstName,
                'middle' : self.middleName,
                'last' : self.lastName,
                'suffix' : self.suffixName
            }

    def drawTextBox(self):
        return """<input type='text' 
    name='%s' 
    id='%s' 
    %s 
    %s 
    value='%s' />""" % (
            self.name,
            self.htmlID,
            self.drawHtmlAttrs(),
            self.drawJSEvents(),
            self.value
        )

