__all__ = ['Link']
from Control import Control

class Link(Control):
    link = None
    target = None
    jsFunc = None
    encode = True
    
    def __init__(self, *a, **k):
        Control.__init__(self, *a, **k)
        self.queryStringDict = {}
        
    def addQSVar(self, name, field=''):
        self.queryStringDict[name] = field

    def drawLink(self):
        qs = {}
        if self.link is not None:
            for k, v in self.queryStringDict.items():
                qs[k] = self.ds.get(v, '')
            if self.ds is not None and hasattr(self.ds, 'externalLink'):
                return self.ds.externalLink(self.link, qs)
            else:
                return self.link
        elif self.jsFunc is not None:
            out = []
            for k, v in self.queryStringDict.items():
                k = str(k)
                if v:
                    out.append('"%s"' % self.ds.get(v, ''))
                else:
                    if len(k) and k[0] == ':':
                        out.append(k[1:])
                    else:
                        out.append('"%s"' % k)
            return "javascript:%s(%s)" % (self.jsFunc, ", ".join(out))
    
    def drawLinkTagOpen(self):
        self.addHtmlAttr('href', self.drawLink())
        if self.target is not None:
            self.addHtmlAttr('target', self.target)

        return "<a %s>" % self.drawHtmlAttrs()

    def drawLinkTagClose(self):
        return "</a>"
        
    def draw(self):
        if self.link is not None or self.jsFunc is not None:
            return "%s%s%s" % (self.drawLinkTagOpen(), self.drawControl(), self.drawLinkTagClose())
        else:
            return self.drawControl()

    def drawControl(self):
        if self.encode:
            return self.htmlEncode(self.value)
        else:
            return str(self.value)
