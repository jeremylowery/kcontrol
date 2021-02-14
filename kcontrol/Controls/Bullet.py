from .RepeaterControl import RepeaterControl

class Bullet(RepeaterControl):
    _mode     = 'disc' # disc, square, circle, number, lower, upper, roman_lower, roman_upper
    modeMap = {
        'disc' : 'disc',
        'square' : 'square',
        'circle' : 'circle',
        'number' : '1',
        'lower' :    'a',
        'upper'    : 'A',
        'roman_lower' : 'i',
        'roman_upper' : 'I'
    }
    _doc_mode = """
        Mode represents the List type.
        Allowed list types are:
            * disc (ul)
            * square (ul)
            * circle (ul)
            * number (ol)
            * lower (ol)
            * upper (ol)
            * roman_lower (ol)
            * roman_upper (ol)
    """
    def get_mode(self):
        if self._mode in ['disc', 'square', 'circle']:
            list_type = 'ul'
        else:
            list_type  = 'ol'
        return list_type
    def set_mode(self, mode):
        self._mode = mode
    mode = property(get_mode, set_mode, doc=_doc_mode)


    def getType(self):
        try:
            return self.modeMap[self._mode]
        except KeyError:
            raise ValueError("Invalid mode \"%s\" Valid modes are  disc, square, circle, number, lower, upper, roman_lower or roman_upper" % self.mode)

    def drawHeader(self):
        return "<%s type='%s' %s>" % (self.mode, self.getType(), self.drawHtmlAttrs())
        
        
    def drawFooter(self):
        return "</%s>\n" % self.mode

    def drawControls(self):
        tar = []
        for ctrl in self._ctrls:
            tar.append('    <li>')
            try:
                tar.append('     %s' % ctrl.draw())
            except AttributeError:
                tar.append('     %s' % ctrl)
            tar.append('    </li>')
        return '\n'.join(tar)
