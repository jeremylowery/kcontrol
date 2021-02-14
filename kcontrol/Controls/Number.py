"""
Added number control.
Primary Options:
    decimals
    
Example:
    num = Number('name','Caption')
    num.decimals = 3
    num.render()
    
    input:
        1.4567
     will yeild:
        1.457

"""

__all__ = ['Number']
from kcontrol.Controls.TextBox import TextBox
from decimal import Decimal

class Number(TextBox):
    decimals = 0 # number of decimal places
    defaultValue = None

    right_align = True
    def buildResources(self):
        self.pushResourceUp('js', 'number_control.js')
        lookup = {'decimals' : self.decimals,
                  'name' : self.name}
        if self.right_align:
            self.addHtmlAttr('style', 'text-align:right;')
        self.addJSEvent("onblur", "formatNumber('%(name)s', %(decimals)s) " %
            lookup)                 

        if self.value is None:
            pass
        else:
            self.value = self.format_string() % self.value
        TextBox.buildResources(self)

    def _get_value(self):
        v = super(Number, self)._get_value()
        if v:
            return int(v)
        else:
            return 0

    value = property(_get_value, TextBox._set_value)

    @property
    def VIEW(self):
        """ Returns the str rep of the value.
        This may be overriden to do formatting for print views of the data.
        """
        if self.value is None:
            return ''
        try:
            value = Decimal(str(self.value))
            if value < 0:
                return "<span style='color:#FF0000;'>%s</span>" % \
                    self.format_string() % value
            else:
                return self.format_string() % value
        except:
            return 'ERROR: %s' % self.value


    def format_string(self):
        if self.decimals == 0:
            return "%d"
        elif self.decimals > 0:
            return "%%.0%sf" % self.decimals
        else:
            raise ValueError('decimals must be a natural number')
