
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
        
