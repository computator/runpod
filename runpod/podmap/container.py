from __future__ import absolute_import, print_function, unicode_literals
import re

from runpod.podmap.image import ImageBase

class Container(object):
    def __init__(self, image, name=None):
        if not isinstance(image, ImageBase):
            raise TypeError("image: expected {} but got {}".format(ImageBase.__name__, type(image).__name__))
        self.image = image
        if name is not None:
            if not isinstance(tag, six.text_type):
                raise TypeError("tag: expected {} but got {}".format(six.text_type.__name__, type(tag).__name__))
            self.name = name
        else:
            match = re.match('(?:.*/)?([^/:]*)(?::.*)?', image.id)
            if match:
                self.name = match.group(1)
            else:
                raise RuntimeError("Image ID '{0.id}' for image {0} does not match expected format".format(image))

    def __repr__(self):
        return "<{} name:'{}' image:{}>".format(__class__.__name__, self.name, self.image)