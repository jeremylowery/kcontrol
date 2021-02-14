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
