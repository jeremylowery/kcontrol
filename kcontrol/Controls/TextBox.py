__all__ = ['TextBox']
from .FormControl import FormControl

class TextBox(FormControl):
    inputType = 'text'
    size = 1
    mask = False
    length = 0
    maxlength = 0
    
    def preRender(self):
        FormControl.preRender(self)
        if self.mask == True:
            self.inputType = 'password'
            
    def _get_htmlAttrs(self):
        attrs = FormControl._get_htmlAttrs(self)
        if 'id' not in attrs:
            attrs['id'] = self.htmlID
        if 'name' not in attrs:
            attrs['name'] = self.name
        if self.length:
            attrs['size'] = self.length
        if self.maxlength:
            attrs['maxlength'] = self.maxlength
        return attrs
    htmlAttrs = property(_get_htmlAttrs, doc=FormControl._doc_htmlAttrs)

    def draw(self):
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
