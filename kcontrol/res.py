from .util import UniqueList

class ResWatcher(object):
    _css = UniqueList()
    _js = UniqueList()

    def __call__(self, res_type, res):
        try:
            attr = getattr(self, "_%s" % res_type)
            attr.append(res)
        except AttributeError:
            pass

    @property
    def css(self):
        return self._css

    @property
    def js(self):
        return self._js
ResWatcher = ResWatcher()

