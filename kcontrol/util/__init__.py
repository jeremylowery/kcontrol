""" Miscallenous utilities """

# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.
import sys


# We use byte strings in python 2 and strings in python 3
if sys.version_info[0] < 3:
    from cStringIO import StringIO
else:
    from io import StringIO

__all__ = ['syncmethod', 'fs2val', 'dict2qs', 'HasIcon', 'UniqueList']

from .syncmethod import syncmethod
from .UniqueList import UniqueList

def str2bool(value):
    if not isinstance(value, str):
        return bool(value)
    value = value.upper().strip()
    if value in ('FALSE', 'NO', 'N', 'DISABLED', '0', ''):
        return False
    return bool(value)

def get_kcontrol_resources(search):
    """ Retrieves all of the javascript and css resources
    from a list of kcontrol's.
    """
    from kcontrol.Controls import Control
    from kcontrol.errors import NotFoundError
    js, inline_js, css, inline_css = [], [], [], []
    for ctrl in search.values():
        if isinstance(ctrl, Control):
            ctrl.preRender()
            try:
                css.extend(ctrl.getResource('css'))
            except NotFoundError:
                pass
            try:
                inline_css.extend(ctrl.getResource('inline_css'))
            except NotFoundError:
                pass
            try:
                js.extend(ctrl.getResource('js'))
            except NotFoundError:
                pass
            try:
                inline_js.extend(ctrl.getResource('inline_js'))
            except NotFoundError:
                pass
    return js, inline_js, css, inline_css

def build_res_strings(js, inline_js, css, inline_css):
      """ Builds a dictionary of strings suitable for embedding in HTML """
      return{
                'kcontrol_js' : "\n".join(["<script type='text/javascript' src='%s'></script>" % j for j in js]),
                'kcontrol_inline_js' : "<script type='text/javascript'>%s</script>" % "\n".join(inline_js),
                'kcontrol_css' : "\n".join(["<link type='text/css' href='%s' rel='stylesheet'></script>" % c for c in css]),
                'kcontrol_inline_css' : "<style type='text/css'>%s</style>" % "\n".join(inline_css)
            }
def fs2val(value):
	""" Translates a value into a simple python value from a field storage deal.
	"""
	if type(value) is str:
		return value
	if hasattr(value, 'value'):
		return value.value
	if type(value) is list:
		return map(fs2val, value)

def dict2qs(d):
	out = []
	for k, v in d.items():
		out.append("%s=%s" % (k, v))
	return "&".join(out)


class HasIcon(object):
    def _get_icon(self):
        """ Returns the 'default' image for the guy """
        if not hasattr(self, 'data') or not self.data:
            return None

        pats = {'icon_small' : '16x16', 'icon_medium' : '22x22', 'icon_large' : '32x32'}
        for p in pats:
            if p in self.data:
                return 'Skin/res/images/icons/%s/%s' % (pats[p], self.data[p])
        return None
    icon = property(_get_icon)
