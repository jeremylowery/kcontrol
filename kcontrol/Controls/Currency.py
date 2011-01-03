
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

from decimal import Decimal
from kcontrol.url import res
from kcontrol.Controls.TextBox import TextBox
__all__ = ['Currency']

class Currency(TextBox):
    inputType = 'text'
    size = 1
    mask = False
    hideSign = False
    defaultValue = None

    def buildResources(self):
        self.pushResourceUp('js', res('Currency/js/currency_control.js'))
        self.addJSEvent("onchange", 'formatCurrency(this, %d);' % self.hideSign)
        self.addHtmlAttr('style', 'text-align:right;')
        TextBox.buildResources(self)

    def draw(self):
        # fix for cheetah useage
        if not self.value:
            self.value = self.defaultValue
        if self.value:
            if isinstance(self.value, str):
                self.value = Decimal(self.value
                    .replace('$', '')
                    .replace(',', ''))
            self.value = '%.02f' % self.value
        return TextBox.draw(self)

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
                value = abs(value)
                return "<span style='color:#FF0000;'>$%.02f</span>" % value
            else:
                return '$%.02f' % value
        except:
            return 'ERROR: %s' % self.value
