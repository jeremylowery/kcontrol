import html
from .FormControl import FormControl

class ListBox(FormControl):
    _vals_built = False
    blankOption = False
    size = 1
    multiple = False

    def __init__(self, name=None, caption='', blankOption=False, *a, **kwargs):
        if 'values' in kwargs:
            self.values = list(kwargs['values'])
            del kwargs['values']
        else:
            self.values = []
        FormControl.__init__(self, name, caption, *a, **kwargs)
        self.blankOption = blankOption

    def _get_htmlAttrs(self):
        attrs = FormControl._get_htmlAttrs(self)
        if self.multiple:
            attrs['multiple'] = 'multple'
        attrs['size'] = str(self.size)
        return attrs
    htmlAttrs = property(_get_htmlAttrs, doc=FormControl._doc_htmlAttrs)

    def preRender(self):
        FormControl.preRender(self)
        if not self._vals_built:
            self.buildValues()

    def buildValues(self):
        self._vals_built = True

    def addValue(self, value, caption):
        self.values[value] = caption

    def draw(self):
        jscript = None
        jscript = '\n'.join(self._resourcesUp.get('inline_js', []))
        if jscript:
            jscript = """
<script langauge='javascript'>
%s
</script>""" % jscript
        return "%s<select %s %s>\n%s\n</select>\n%s" % (
            self.drawShadowControl(),
            self.drawHtmlAttrs(),
            self.drawJSEvents(),
            self.drawOptions(),
            jscript
        )

    def drawOptions(self):
        opts = []
        if self.blankOption:
            opts.append("<option value=''></option>")
        if not isinstance(self.value, list):
            values = [str(self.value)]
        else:
            values = [str(s) for s in self.value]

        for value, caption in self.values:
            opts.append('<option value="%s" %s>%s</option>' % (
                html.escape(str(value), True),
                value in values and "selected='selected'" or '',
                html.escape(str(caption))
            ))
        return '\n'.join(opts)

class StateListBox(ListBox):
    def __init__(self, name=None, caption='', *a, **k):
        FormControl.__init__(self, name, caption, *a, **k)
        self.values = [
            ("", ""),
            ("AL", "Alabama"),
            ("AK", "Alaska"),
            ("AZ", "Arizona"),
            ("AR", "Arkansas"),
            ("CA", "California"),
            ("CO", "Colorado"),
            ("CT", "Connecticut"),
            ("DE", "Delaware"),
            ("DC", "District of Columbia"),
            ("FL", "Florida"),
            ("GA", "Georgia"),
            ("HI", "Hawaii"),
            ("ID", "Idaho"),
            ("IL", "Illinois"),
            ("IN", "Indiana"),
            ("IA", "Iowa"),
            ("KS", "Kansas"),
            ("KY", "Kentucky"),
            ("LA", "Louisiana"),
            ("ME", "Maine"),
            ("MD", "Maryland"),
            ("MA", "Massachusetts"),
            ("MI", "Michigan"),
            ("MN", "Minnesota"),
            ("MS", "Mississippi"),
            ("MO", "Missouri"),
            ("MT", "Montana"),
            ("NE", "Nebraska"),
            ("NV", "Nevada"),
            ("NH", "New Hampshire"),
            ("NJ", "New Jersey"),
            ("NM", "New Mexico"),
            ("NY", "New York"),
            ("NC", "North Carolina"),
            ("ND", "North Dakota"),
            ("OH", "Ohio"),
            ("OK", "Oklahoma"),
            ("OR", "Oregon"),
            ("PA", "Pennsylvania"),
            ("RI", "Rhode Island"),
            ("SC", "South Carolina"),
            ("SD", "South Dakota"),
            ("TN", "Tennessee"),
            ("TX", "Texas"),
            ("UT", "Utah"),
            ("VT", "Vermont"),
            ("VA", "Virginia"),
            ("WA", "Washington"),
            ("WV", "West Virginia"),
            ("WI", "Wisconsin"),
            ("WY", "Wyoming")]

