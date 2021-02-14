__all__ = ['TextArea']
from .FormControl import FormControl

class TextArea(FormControl):
    inputType = 'text'
    size = 5
    cols = 50
    mask = False
    wrap = 'soft'
    
    def preRender(self):
        FormControl.preRender(self)
        if self.mask == True:
            self.inputType = 'password'
            
    def draw(self):
        # fix for cheetah useage
        if not self.value:
            self.value = self.defaultValue
         
        self.addHtmlAttr('wrap', self.wrap)

        if self.size == 1:
            return FormControl.draw(self)
        if self.mask:
            raise ValueError("A control cannot have a size greater than one and a mask property of True")
        
        if self.value:
            value = self.value
        else:
            value = ''
        return "<textarea name='%s' id='%s' rows='%s' cols='%s' %s %s>%s</textarea>" % (
            self.name,
            self.htmlID,
            self.size,
            self.cols,
            self.drawHtmlAttrs(),
            self.drawJSEvents(),
            value
        )
