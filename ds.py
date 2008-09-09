
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

import cgi
import copy
import kg.mapping
import threading
import UserDict

__all__ = ['DS', 'SingleValueDS', 'RepeatDS']

store = kg.mapping.ThreadDict()

def from_fs(fs=None):
    global store
    if fs is None:
        fs = cgi.FieldStorage()
    for key in fs.keys():
        store[key] = fs.getvalue(key)

class DS(object):
	"""A data source provided to a control which provides values.
	Data sources are dictionary-like objects. Subclasses can implement
	_get_KEY methods to have their values automatically resolved using
	dictionary lookup syntax. """
	def __init__(self, dict=None):
		self.data = {}
		if dict is not None: 
			self.update(dict)

	def __cmp__(self, dict):
		if isinstance(dict, DS):
			return cmp(self.data, dict.data)
		else:
			return cmp(self.data, dict)

	def __len__(self): 
		return len(self.data)

	def __call__(self, *a):
		return map(lambda x: self[x], a)
	
	def __getitem__(self, name):
		try:
			return self.data[name]
		except KeyError:
			try:
				attr = getattr(self, '_get_%s' % name)
			except AttributeError:
				raise KeyError, name
			return attr()
	
	def __setitem__(self, key, item):
		try:
			attr = getattr(self, '_set_%s' % key)
		except AttributeError:
			self.data[key] = item
		else:
			attr(item)
	
	def __delitem__(self, key): 
		del self.data[key]

	def clear(self): 
		self.data.clear()

	def copy(self):
		if self.__class__ is DS:
			return DS(self.data)
		data = self.data
		try:
			self.data = {}
			c = copy.copy(self)
		finally:
			self.data = data
		c.update(self)
		return c

	def copyFrom(self, ds):
		map(lambda s: self.__setitem__(s, ds[s]), ds.keys())
		
	def _dict_methods(self):
		""" Retrieves the "dictionary hook" methods that an object supports """
		d = filter(lambda s: s.startswith("_get_"), dir(self))
		d = filter(lambda s: s, map(lambda s: s[5:], d))
		return d

	def keys(self):
		return self.data.keys() + self._dict_methods()

	def items(self): 
		items = self.data.items()
		for method in self._dict_methods():
			items.append((method, self[method]))
			
	def update(self, dic):
		[self.__setitem__(key, dic[key]) for key in dic]
		
	def values(self): 
		values = self.data.values()
		for method in self._dict_methods():
			values.append(self[method])

	def has_key(self, key):
		return key in self.keys()

	def get(self, key, failobj=None):
		if not self.has_key(key):
			return failobj
		return self[key]
	
	def setdefault(self, key, failobj=None):
		if not self.has_key(key):
			self[key] = failobj
		return self[key]

	def popitem(self):
		return self.data.popitem()

	def __contains__(self, key):
		return key in self.keys()

class SingleValueDS(DS):
	"""A data source which always returns the same value

	This data source is useful for very simple controls like Labels who don't
	really need a "true" data source."""
	def __init__(self, value):
		DS.__init__(self)
		self.value = value
		
	def __getitem__(self, name):
		return self.value

class RepeatDS(DS):
	"""A data source for a repeater control

    Repeat Data sources contain children data sources, which are generated for
    each child control of the Composite Repeat Control that the RepeatDS
    provides for.

    It is convinent for the children of Repeat data sources to be Repeat data
    sources as well. This creates a tree of data sources which map directly (1
    to 1) to the Repeater Control.

    Repeater Controls usually require more information from their data source
    then standard Controls. More commonly than not, a composite control will not
    know the exact nature of the data source being provided to it.

    Examples of this case include:
     - A Pager does not know before hand the fields that are displayed in each
       row
     - A Calendar does not know all of the properties that a calendar entry may
       have but will still need to display them.
	   
    As such, the Repeat Data Sources provides a fields attribute which contains
    the fields that the data source provides.

    More times than not, the root data source will not provide this information,
    but the children will."""

	def __init__(self, build_children=True, children=None, *a, **k):
		DS.__init__(self, *a, **k)
		if not children:
			children = []
		self._children = children
		if build_children:
			self.buildChildren()
	
	def buildChildren(self):
		""" Build the children for the repeat data source
		
		Override this method and use the addChild method to
		add child data sources to the RepeatDS
		"""
		pass
	
	def addChild(self, ds):
		if self._children is None:
			self._children = []
		self._children.append(ds)
		
	def children(self):
		if self._children is None:
			self._children = []
			self.buildChildren()
		return tuple(self._children)
	children = property(children)
