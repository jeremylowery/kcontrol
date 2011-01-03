import compiler
import datetime
import locale
import re
import time
import urllib

def unrepr(s):
    """ Parses a string representation of a python data structure and
    returns the python object. This is safer than eval because it only
    works with built-in syntactic data structures.
    """
    if not s:
        return s
    elif not isinstance(s, basestring):
        # passthru real objects
        return s
    try:
        return _Builder().build(_getObj(s))
    except (UnknownType, SyntaxError):
        return s

def _getObj(s):
    s = "a=" + s
    p = compiler.parse(s)
    return p.getChildren()[1].getChildren()[0].getChildren()[1]

class UnknownType(Exception):
    pass

class _Builder:
    def build(self, o):
        m = getattr(self, 'build_' + o.__class__.__name__, None)
        if m is None:
            raise UnknownType(o.__class__.__name__)
        return m(o)

    def build_List(self, o):
        return map(self.build, o.getChildren())

    def build_Const(self, o):
        return o.value

    def build_Dict(self, o):
        d = {}
        i = iter(map(self.build, o.getChildren()))
        for el in i:
            d[el] = i.next()
        return d

    def build_Tuple(self, o):
        return tuple(self.build_List(o))

    def build_Name(self, o):
        if o.name == 'None':
            return None
        if o.name == 'True':
            return True
        if o.name == 'False':
            return False

        # See if the Name is a package or module
        #try:
        #    return modules(o.name)
        #except ImportError:
        #    pass

        raise UnknownType(o.name)

    def build_Add(self, o):
        real, imag = map(self.build_Const, o.getChildren())
        try:
            real = float(real)
        except TypeError:
            raise UnknownType('Add')
        if not isinstance(imag, complex) or imag.real != 0.0:
            raise UnknownType('Add')
        return real+imag

    def build_Getattr(self, o):
        parent = self.build(o.expr)
        return getattr(parent, o.attrname)



FUNC_CALL_EXP = re.compile(r'^([a-zA-Z][a-zA-Z_0-9]*)\((.*?)\)$')

def parse_function_call(val, FUNC_CALL_EXP=FUNC_CALL_EXP):
    """ Given a function call expression, return the function name and
    the argument list.

    parse_function_call("foo(1, 2)") -> ("foo", (1, 2))
    """
    val = val.strip()
    pat = FUNC_CALL_EXP.match(val)
    if pat:
        fun_name, fun_args = pat.groups()
        args = unrepr("(%s,)" % fun_args)
        return fun_name, args
    elif not re.match('\w+', val):
        raise ValueError, 'Invalid expression %r' % val
    else:
        return val, ()
