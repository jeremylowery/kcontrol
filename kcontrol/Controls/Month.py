from kcontrol.Controls.ListBox import ListBox
import datetime

class Month(ListBox):
    def __init__(self, name=None, caption='', *a, **k):
        ListBox.__init__(self, name, caption, *a, **k)

        for i in range(1, 13):
            self.values.append((i, i))

        self.defaultValue = datetime.datetime.now().month

