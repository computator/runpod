from __future__ import absolute_import, print_function, unicode_literals
import attr
import re
import six

from runpod.podmap.image import ImageBase

@attr.s(repr=False)
class Container(object):
    image = attr.ib(validator=attr.validators.instance_of(ImageBase))
    name = attr.ib(validator=attr.validators.instance_of(six.text_type))

    @name.default
    def _name_def(self):
        match = re.match('(?:.*/)?([^/:]*)(?::.*)?', self.image.id)
        if match:
            return match.group(1)
        raise RuntimeError("Image ID '{0.id}' for image {0} does not match expected format".format(self.image))

    annotations = attr.ib(factory=dict, init=False)
    extra_hosts = attr.ib(factory=dict, init=False)
    capabilities_add = attr.ib(default=set, init=False)
    capabilities_drop = attr.ib(default=set, init=False)
    devices = attr.ib(factory=list, init=False)
    dns_enabled = attr.ib(default=True, init=False)
    dns_options = attr.ib(factory=dict, init=False)
    dns_search = attr.ib(factory=list, init=False)
    dns_servers = attr.ib(factory=list, init=False)
    entrypoint = attr.ib(default=None, init=False)
    env = attr.ib(factory=dict, init=False)
    env_file = attr.ib(default=None, init=False)
    exposed_ports = attr.ib(default=set, init=False)
    hostname = attr.ib(default=None, init=False)
    ip = attr.ib(default=None, init=False)
    labels = attr.ib(factory=dict, init=False)
    label_file = attr.ib(default=None, init=False)
    mounts = attr.ib(factory=list, init=False)
    network = attr.ib(default=None, init=False)
    no_hosts = attr.ib(default=False, init=False)
    privileged = attr.ib(default=False, init=False)
    publish = attr.ib(factory=list, init=False)
    publish_all = attr.ib(default=False, init=False)
    read_only = attr.ib(default=False, init=False)
    security_opts = attr.ib(factory=list, init=False)
    tmpfs_mounts = attr.ib(factory=list, init=False)
    user = attr.ib(default=None, init=False)
    volumes = attr.ib(factory=list, init=False)
    volumes_from = attr.ib(default=None, init=False)
    working_directory = attr.ib(default=None, init=False)

    def __repr__(self):
        return "{}(name={!r}, image={!r}>".format(type(self).__name__, self.name, self.image)