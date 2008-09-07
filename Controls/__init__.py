"""
Usage Example
=============

    jlee@spike kcontrol $ python
    Python 2.4.4c1 (#2, Oct 11 2006, 21:51:02)
    [GCC 4.1.2 20060928 (prerelease) (Ubuntu 4.1.1-13ubuntu5)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import kcontrol
    >>> fn = kcontrol.TextBox('first_name')
    >>> phone = kcontrol.Phone('phone')
    >>> print phone
    <input type='text' value='' id='phone' name='phone' onblur='setPhone("phone")' />
    >>> print fn
    <input type='text' value='' id='first_name' name='first_name'  />

To-Do
=====

The kcontrol configuration must be threaded some how so that the controls can reference it, but user's preferences may remain different.
Date, Name, and Time should then pull their default formats from the config.

A resource watcher needs hooked into kcontrols, to catch css and js pushed up.
res.py is an example of the ResWatcher API.  Feel free to edit this "ResWatcher"  in any means necessary so long as the call signature is maintained.
    
"""
