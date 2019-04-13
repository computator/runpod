from __future__ import absolute_import, print_function, unicode_literals

from runpod.podmap.container import Container

class Pod(object):
    def __init__(self, containers=None):
        if containers:
            containers = list(containers)
            if any(True for ctr in containers if not isinstance(ctr, Container)):
                raise TypeError("'containers' must be an iterable of {} instances".format(Container.__name__))
            self.containers = containers
        else:
            self.containers = []

    def __repr__(self):
        return '<{} containers:{!r}>'.format(__class__.__name__, self.containers)

    def add_container(self, container):
        if not isinstance(container, Container):
            raise TypeError("{!r} is not a {} instance".format(container, Container.__name__))
        self.containers.append(container)