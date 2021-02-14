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
