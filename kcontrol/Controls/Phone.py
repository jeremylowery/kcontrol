"""
    Formats > 10 digit : (xxx) xxx-xxxx ext: x2
    Formats 10 digit   : (xxx) xxx-xxxx
    Fomats 7 diget     : xxx-xxxx   
    Igores everything else
"""
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
