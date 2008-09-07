
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

from kcontrol.util import OrderedDict
from FormControl import FormControl

class ListBox(FormControl):
    values = OrderedDict()
    _vals_built = False
    blankOption = False
    size = 1
    multiple = False

    def __init__(self, name=None, caption='', *a, **kwargs):
        if 'values' in kwargs:
            self.values = OrderedDict()
            for k, v in kwargs['values']:
                self.values[k] = v
            del kwargs['values']
            #kwargs = dict(i for i in kwargs.items() if i[0] != 'values')
        else:
            self.values = OrderedDict()
        FormControl.__init__(self, name, caption, *a, **kwargs)

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
        for value, caption in self.values.items():
            opts.append("<option value='%s' %s>%s</option>" % (
                value,
                str(value) == str(self.value) and "selected='selected'" or '',
                caption
            ))
        return '\n'.join(opts)

    def sleep(self, trans=None):
        FormControl.sleep(self, trans)
        self.values = OrderedDict()

class StateListBox(ListBox):
    def __init__(self, name=None, caption='', *a, **k):
        FormControl.__init__(self, name, caption, *a, **k)
        values = OrderedDict()
        values[""] = ""
        values["AL"] = "Alabama"
        values["AK"] = "Alaska"
        values["AZ"] = "Arizona"
        values["AR"] = "Arkansas"
        values["CA"] = "California"
        values["CO"] = "Colorado"
        values["CT"] = "Connecticut"
        values["DE"] = "Delaware"
        values["DC"] = "District of Columbia"
        values["FL"] = "Florida"
        values["GA"] = "Georgia"
        values["HI"] = "Hawaii"
        values["ID"] = "Idaho"
        values["IL"] = "Illinois"
        values["IN"] = "Indiana"
        values["IA"] = "Iowa"
        values["KS"] = "Kansas"
        values["KY"] = "Kentucky"
        values["LA"] = "Louisiana"
        values["ME"] = "Maine"
        values["MD"] = "Maryland"
        values["MA"] = "Massachusetts"
        values["MI"] = "Michigan"
        values["MN"] = "Minnesota"
        values["MS"] = "Mississippi"
        values["MO"] = "Missouri"
        values["MT"] = "Montana"
        values["NE"] = "Nebraska"
        values["NV"] = "Nevada"
        values["NH"] = "New Hampshire"
        values["NJ"] = "New Jersey"
        values["NM"] = "New Mexico"
        values["NY"] = "New York"
        values["NC"] = "North Carolina"
        values["ND"] = "North Dakota"
        values["OH"] = "Ohio"
        values["OK"] = "Oklahoma"
        values["OR"] = "Oregon"
        values["PA"] = "Pennsylvania"
        values["RI"] = "Rhode Island"
        values["SC"] = "South Carolina"
        values["SD"] = "South Dakota"
        values["TN"] = "Tennessee"
        values["TX"] = "Texas"
        values["UT"] = "Utah"
        values["VT"] = "Vermont"
        values["VA"] = "Virginia"
        values["WA"] = "Washington"
        values["WV"] = "West Virginia"
        values["WI"] = "Wisconsin"
        values["WY"] = "Wyoming"
        self.values = values

