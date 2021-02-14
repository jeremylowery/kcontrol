
__all__ = ['FilePicker']
from .FormControl import FormControl

class FilePicker(FormControl):
    inputType = 'file'

    def buildResources(self):
        self.pushResourceUp('html_enctype', 'form/multi-part')
