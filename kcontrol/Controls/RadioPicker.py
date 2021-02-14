import cgi
from kcontrol.util import StringIO
from .FormControl import FormControl

class RadioPicker(FormControl):
    _vals_built = False

    def __init__(self, name=None, caption='', values=[], *a, **kwargs):
        self.values = values
        FormControl.__init__(self, name, caption, *a, **kwargs)

    def preRender(self):
        FormControl.preRender(self)
        if not self._vals_built:
            self.buildValues()

    def buildValues(self):
        self._vals_built = True

    def addValue(self, value, caption):
        self.values.append((caption, value))

    def draw(self):
        buf = StringIO()
        jscript = '\n'.join(self._resourcesUp.get('inline_js', []))
        if jscript:
            buf.write("<script langauge='javascript'>\n")
            buf.write(jscript)
            buf.write("</script>")
        buf.write(self.drawShadowControl())
        for caption, value in self.values:
            cvalue = cgi.escape(value, True)
            cname = cgi.escape(self.name, True)
            html_id = "%s_%s_%s" % (self.name, caption, value)
            html_id = cgi.escape(html_id, True)

            buf.write("<input type='radio' value='%s' id='%s' " %
                      (cvalue, html_id))
            buf.write("name='%s' " % cname)
            if str(value) == str(self.value):
                buf.write("checked='checked' ")
            buf.write("/><label for='%s'>%s</label></option>" % 
                (html_id, caption))

        buf.seek(0)
        return buf.getvalue()


