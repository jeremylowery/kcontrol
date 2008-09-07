
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

from threading import RLock

class syncmethod(object):
    """ Descriptor that makes a method call thread safe. That is, only
    one thread will be able to execute the given method at a time, all
    other threads will block. """

    def __init__(self, method):
        self._method = method
        self._lockname = '__syncmethodlock%s__' % method.__name__

    def __get__(self, inst, type=None):
        if not hasattr(inst, self._lockname):
            setattr(inst, self._lockname, RLock())
        lock = getattr(inst, self._lockname)
        return SyncMethodWrapper(inst, self._method, lock)

    def __set__(self, inst, value, type=None):
        raise AttributeError, self._method.__name__

    #def __del__(self):
    #    raise AttributeError, self._method.__name__

class SyncMethodWrapper:
    def __init__(self, inst, method, lock):
        self._inst = inst
        self._method = method
        self._lock = lock

    def __call__(self, *args, **kwargs):
        self._lock.acquire()
        try:
            return apply(self._method, (self._inst,) + args, kwargs)
        finally:
            self._lock.release()

if __name__ == '__main__':
    class Test(object):
        def __init__(self):
            self.value = 0
        def doit(self):
            self.value = self.value + 1
            print self.value
        doit = syncmethod(doit)

    def slam(inst):
        for x in range(100):
            inst.doit()

    t = Test()
    from threading import Thread, Lock
    ts = []
    for x in range(5):
        ts.append(Thread(target=slam, args=(t,)))

    for x in ts:
        x.start()
    for x in ts:
        x.join()
