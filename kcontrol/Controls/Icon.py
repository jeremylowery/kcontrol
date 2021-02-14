###############################################################################
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license
# 
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.
###############################################################################
__all__ = ['Icon']

from .Link import Link

class Icon(Link):
    """ The icon control just has an icon. yay """
    def buildResources(self):
        Link.buildResources(self)
        self.addHtmlAttr('border', '0')

    def drawControl(self):
        value = self.value or self.name
        return "<img src='%s' alt='%s' title='%s' %s %s />" % (
            value, 
            self.caption, 
            self.caption,
            self.drawHtmlAttrs(),
            self.drawJSEvents()
        )
