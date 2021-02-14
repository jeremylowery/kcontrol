from kcontrol.Controls.Control import Control
from kcontrol.Controls.Label import Label

class FormControl(Control):
    inputType = 'text'
    shadowControl = False
    showCaption = True
    tabindex = None

    def _get_htmlID(self):
        return self.name
    htmlID = property(_get_htmlID)

    def _get_htmlAttrs(self):
        attrs = Control._get_htmlAttrs(self)
        if 'id' not in attrs:
            attrs['id'] = self.htmlID
        if 'name' not in attrs:
            attrs['name'] = self.name
        if 'tabindex' not in attrs and self.tabindex is not None:
            attrs['tabindex'] = self.tabindex
        return attrs
    htmlAttrs = property(_get_htmlAttrs, doc=Control._doc_htmlAttrs)

    def _get_caption(self):
        label = Label(caption=self._caption)
        label.ds = self.name
        return label.render()
    caption = property(_get_caption, Control._set_caption)

    def draw(self):
        # fix for cheetah useage
        if not self.value:
            self.value = self.defaultValue
        
        jscript = None
        jscript = '\n'.join(self._resourcesUp.get('inline_js', []))
        if jscript:
            jscript = """
<script langauge='javascript'>
%s
</script>""" % jscript
        if self.shadowControl:
            buf = '<input type="hidden" name="%s" value="" />' % self.name
        else:
            buf = ''

        return """%s<input type="%s" %s %s %s />%s""" % (
            self.drawShadowControl(),
            self.inputType,
            self.drawValueAttr(),
            self.drawHtmlAttrs(),
            self.drawJSEvents(),
            jscript
        )

    def drawShadowControl(self):
        if self.shadowControl:
            return '<input type="hidden" name="%s" value="" />' % self.name
        else:
            return ''

    def drawValueAttr(self):
        return 'value="%s"' % self.htmlEncode(self.value)

    def findForm(self):
        """ Seaches up the control hierarchy for the form that the form control is a member of """
        from Form import Form
        parent = self.parent
        while True:
            if isinstance(parent, Form):
                if parent.showFormTag:
                    return parent
            elif parent is None:
                return None
            parent = parent.parent
