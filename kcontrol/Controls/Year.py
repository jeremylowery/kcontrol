import datetime
from .ListBox import ListBox

class Year(ListBox):
    def __init__(self, name=None, caption='', *a, **k):
        ListBox.__init__(self, name, caption, *a, **k)
        year = datetime.datetime.now().year
        for i in range(year-10, year+10):
            self.values.append((i, i))
        self.defaultValue = year
