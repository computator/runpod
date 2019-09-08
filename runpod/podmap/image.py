from __future__ import absolute_import, print_function, unicode_literals
import abc
import attr
import os.path
import six
from six.moves.urllib import parse as urllib_parse

@six.add_metaclass(abc.ABCMeta)
@attr.s
class ImageBase(object):
    @abc.abstractproperty
    def id(self):
        pass

@attr.s
class DockerfileImage(ImageBase):
    source = attr.ib(validator=attr.validators.instance_of(six.text_type))

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

@attr.s
class NamedImage(ImageBase):
    image = attr.ib(validator=attr.validators.instance_of(six.text_type))
    tag = attr.ib(default='latest', validator=attr.validators.instance_of(six.text_type))

    @property
    def id(self):
        return "{}:{}".format(self.image, self.tag)
