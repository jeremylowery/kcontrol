# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

from kcontrol.util import OrderedDict
from kcontrol.Controls.ListBox import ListBox
import datetime

class Year(ListBox):
    def __init__(self, name=None, caption='', *a, **k):
        ListBox.__init__(self, name, caption, *a, **k)
        year = datetime.datetime.now().year
        for i in range(year-10, year+10):
            self.values[i] = i
        self.defaultValue = year