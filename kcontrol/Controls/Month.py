# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

from kcontrol.Controls.ListBox import ListBox
import datetime

class Month(ListBox):
    def __init__(self, name=None, caption='', *a, **k):
        ListBox.__init__(self, name, caption, *a, **k)

        for i in range(1, 13):
            self.values.append((i, i))
    
        self.defaultValue = datetime.datetime.now().month

