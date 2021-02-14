__all__ = ['Hidden']
import datetime
from .FormControl import FormControl

class Hidden(FormControl):
    inputType = 'hidden'
    visible = False
    showCaption = False

    def draw(self):
        if isinstance(self.value, datetime.date):
            self.value = self.value.strftime("%Y%m%d")
        return FormControl.draw(self)
