from __future__ import absolute_import, print_function, unicode_literals

import attr
from runpod.podmap.container import Container

@attr.s
class Pod(object):
    containers = attr.ib(factory=list, validator=attr.validators.deep_iterable(attr.validators.instance_of(Container)))

    def add_container(self, container):
        if not isinstance(container, Container):
            raise TypeError("{!r} is not a {} instance".format(container, Container.__name__))
        self.containers.append(container)