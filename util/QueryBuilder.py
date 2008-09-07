
# The contents of this program are subject to the Koar Public License
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.koarcg.com/license

# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# included LICENSE.txt file for more information. Copyright 2007 KCG.

__all__ = ['QueryBuilder']

from cStringIO import StringIO
class QueryBuilder(object):
    table = None
    limit = ''

    def __init__(self):
        self.fields = []
        self.joins = []
        self.conds = []
        self.sorts = []

    def build(self):
        buf = StringIO()
        buf.write("SELECT %s FROM %s " % (",".join(self.fields), self.table))
        buf.write(" ".join(self.joins))
        if self.conds:
            buf.write(" WHERE")
        for i in range(len(self.conds)):
            cond = self.conds[i]
            if i == 0:
                buf.write(" %s" % cond[1])
            else:
                buf.write(" %s %s" % cond)
        if self.sorts:
            buf.write(" ORDER BY ")
            #raise str(self.sorts)
            buf.write(", ".join(self.sorts))
        if self.limit:
            buf.write(" LIMIT %s" % self.limit)
        return buf.getvalue()
