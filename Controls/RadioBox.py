import cgi
import cStringIO
from FormControl import FormControl

class RadioBox(FormControl):
    def __init__(self, name, value2, caption='', *a, **kwargs):
        """ value2 -> the value of the radio box. If the control value
        equals this value, the radio box will be selected.
        """

        self.value2 = value2
        FormControl.__init__(self, name, caption, *a, **kwargs)

    @property
    def htmlID(self):
        return '%s_%s' % (self.name, self.value2)

    def draw(self):
        buf = cStringIO.StringIO()
        jscript = '\n'.join(self._resourcesUp.get('inline_js', []))
        if jscript:
            buf.write("<script langauge='javascript'>\n")
            buf.write(jscript)
            buf.write("</script>")
        
        buf.write("<input type='radio' value='%s' %s" % (self.value2,
                    self.drawHtmlAttrs()))

        if self.value == self.value2:
            buf.write(" checked='checked'")
        buf.write(" />")
        if self.caption:
            buf.write("<label for='%s'>%s</label>" % 
                (self.htmlID, self.caption))

        buf.seek(0)
        return buf.getvalue()

