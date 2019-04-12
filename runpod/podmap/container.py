from __future__ import absolute_import, print_function, unicode_literals

class Container(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{} name:{}>'.format(__class__.__name__, self.name)