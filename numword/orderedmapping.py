#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
orderedmapping
'''

from __future__ import generators


class OrderedMapping(dict):
    '''
    Ordered Mapping
    '''

    def __init__(self, *pairs):
        super(OrderedMapping, self).__init__()
        self.order = []
        for key, val in pairs:
            self[key] = val

    def __setitem__(self, key, val):
        if key not in self:
            self.order.append(key)
        super(OrderedMapping, self).__setitem__(key, val)

    def __iter__(self):
        for item in self.order:
            yield item

    def __repr__(self):
        out = ["%s: %s" % (repr(item), repr(self[item])) for item in self]
        out = ", ".join(out)
        return "{%s}" % out
