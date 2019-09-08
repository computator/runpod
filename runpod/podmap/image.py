from __future__ import absolute_import, print_function, unicode_literals
import abc
import os.path
import six
from six.moves.urllib import parse as urllib_parse

@six.add_metaclass(abc.ABCMeta)
class ImageBase(object):
    @abc.abstractmethod
    def __init__(self):
        pass

    def __repr__(self):
        return '<{}>'.format(type(self).__name__)

    @abc.abstractproperty
    def id(self):
        pass

class DockerfileImage(ImageBase):
    def __init__(self, dockerfile):
        if not isinstance(dockerfile, six.text_type):
            raise TypeError("expected {}, got {}".format(six.text_type.__name__, type(dockerfile).__name__))
        self.source = dockerfile

    def __repr__(self):
        return "<{} source:'{}'>".format(type(self).__name__, self.source)

    @property
    def id(self):
        if '//' in self.source:
            url = urllib_parse.urlparse(self.source)
            if not url.path:
                return six.text_type(url.netloc)
            path = "{}/{}".format(url.netloc, url.path)
        else:
            path = os.path.abspath(self.source)
        return six.text_type(os.path.basename(os.path.dirname(path)))

class NamedImage(ImageBase):
    def __init__(self, image, tag='latest'):
        if not isinstance(image, six.text_type):
            raise TypeError("image: expected {} but got {}".format(six.text_type.__name__, type(image).__name__))
        if not isinstance(tag, six.text_type):
            raise TypeError("tag: expected {} but got {}".format(six.text_type.__name__, type(tag).__name__))
        self.image = image
        self.tag = tag

    def __repr__(self):
        return "<{} ref:'{}:{}'>".format(type(self).__name__, self.image, self.tag)

    @property
    def id(self):
        return "{}:{}".format(self.image, self.tag)
