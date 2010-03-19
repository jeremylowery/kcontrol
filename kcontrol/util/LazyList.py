
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ['LazyList']
from UserList import UserList

class LazyList(UserList):
	def __init__(self, eval, *a, **k):
		UserList.__init__(self, *a, **k)
		self._lazy = {}
		self._evalFunc = eval
	
	def __getitem__(self, item):
		try:
				return self._lazy[item]
		except KeyError:
				self._lazy[item] = self._evalFunc(self.data[item])
				return self._lazy[item]
	
	def __delitem__(self, item):
		UserList.__delitem__(self, item)
		try:
				del self._lazy[item]
		except KeyError:
				pass
	
	def __setitem__(self, item, value):
		try:
				del self._lazy[item]
		except KeyError:
				pass
		UserList.__setitem__(self, item, value)

	def __getslice__(self, i, j):
		i = max(i, 0); j = max(j, 0)
		return self.__class__(self._evalFunc, self.data[i:j])
