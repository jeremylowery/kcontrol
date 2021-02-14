
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
