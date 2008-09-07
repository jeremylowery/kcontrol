
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.


_config = {}

def get(key, default=''):
    global _config
    try:
        return _config[key]
    except KeyError:
        return default

def update(d):
    global _config
    _config.update(d)
    
    
## Register a callback hook into the date time plumbing. 

def register_date_formats(format1, format2):
    class F(object):
        def __init__(self, proc):
            self.proc = proc
            
        def __get__(self, obj, type=None):
            return self.proc()
        
    from kcontrol.DatePicker import DatePicker
    DatePicker.format = F(format1)
    DatePicker.format2 = F(format2)
    
    
""" Register a callback hook into the name format stuff. """
def register_name_format(format):
    class F(object):
        def __init__(self, proc):
            self.proc = proc
            
        def __get__(self, obj, type=None):
            return self.proc()
        
    from kcontrol.NameTextBox import NameTextBox
    NameTextBox.format = F(format)    


def register_resource_hook(proc):
    """ proc is called with type and resource. """
    from kcontrol.Control import Control
    Control._resource_watchers.append(proc)
