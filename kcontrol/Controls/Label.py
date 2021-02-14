
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ['Label']
from .Control import Control

class Label(Control):
    def draw(self):
        if not self.value:
            self.value = self.defaultValue
        caption = self.caption or self.value
        return "<label for='%s'>%s</label>" % (self.name, caption)
