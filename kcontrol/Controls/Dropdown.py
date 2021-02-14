
from .FormControl import FormControl
from kcontrol.util import StringIO

__all__ = ['Dropdown']

class Dropdown(FormControl):
    inputType = 'text'

    def __init__(self, *a, **k):
        self.options = []
        FormControl.__init__(self, *a, **k)

    def preRender(self):
        FormControl.preRender(self)

    def draw(self):
        buf = StringIO()
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
            raise ValueError("A control cannot have a size greater than one and a mask property of True")

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
