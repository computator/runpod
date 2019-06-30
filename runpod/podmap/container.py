from __future__ import absolute_import, print_function, unicode_literals
import re

from runpod.podmap.image import ImageBase

class Container(object):
    def __init__(self, image, name=None):
        if not isinstance(image, ImageBase):
            raise TypeError("image: expected {} but got {}".format(ImageBase.__name__, type(image).__name__))
        self.image = image
        if name is not None:
            if not isinstance(name, six.text_type):
                raise TypeError("name: expected {} but got {}".format(six.text_type.__name__, type(name).__name__))
            self.name = name
        else:
            match = re.match('(?:.*/)?([^/:]*)(?::.*)?', image.id)
            if match:
                self.name = match.group(1)
            else:
                raise RuntimeError("Image ID '{0.id}' for image {0} does not match expected format".format(image))

        self._exposed_ports = set();

    def __repr__(self):
        return "<{} name:'{}' image:{}>".format(__class__.__name__, self.name, self.image)

    @property
    def exposed_ports(self):
        return self._exposed_ports.copy()

    def add_exposed_ports(self, ports):
        ports = list(ports)
        if any(True for port in ports if not isinstance(port, (tuple, int))):
            raise TypeError("ports: iterable can only contain values of type tuple or int")
        for portrange in [port for port in ports if isinstance(port, tuple)]:
            if len(portrange) != 2:
                raise TypeError("ports: tuple port ranges must be of length 2")
            if any(True for port in portrange if not isinstance(port, int)):
                raise TypeError("ports: tuple port ranges can only contain values of type int")
        new_ports = set()
        for port in ports:
            if isinstance(port, tuple):
                if port[0] <= port[1]:
                    raise ValueError("ports: end value must be greater than start in tuple port ranges")
                new_ports.update(range(port[0], port[1]+1))
            else:
                new_ports.add(port)
        self._exposed_ports.update(new_ports)
