
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = [
		    'NotFoundError',
		    'NotImplementedError',
		    'DuplicateError',
		    'ModificationError',
		    'ValidationError'
		   ]

class NotFoundError(Exception):
	pass

class NotImplementedError(Exception):
	pass

class DuplicateError(Exception):
	pass


class ValidationError(Exception):
	pass

class ModificationError(ValidationError):
	def current_access(self):
		return self.args[0]
	def last_access(self):
		return self.args[1]
