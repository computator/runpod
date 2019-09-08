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

        self.annotations = {}
        self.extra_hosts = {}
        self.capabilities_add = set()
        self.capabilities_drop = set()
        self.devices = []
        self.dns_enabled = True
        self.dns_options = {}
        self.dns_search = []
        self.dns_servers = []
        self.entrypoint = None
        self.env = {}
        self.env_file = None
        self.exposed_ports = set()
        self.hostname = None
        self.ip = None
        self.labels = {}
        self.label_file = None
        self.mounts = []
        self.network = None
        self.no_hosts = False
        self.privileged = False
        self.publish = []
        self.publish_all = False
        self.read_only = False
        self.security_opts = []
        self.tmpfs_mounts = []
        self.user = None
        self.volumes = []
        self.volumes_from = None
        self.working_directory = None

    def __repr__(self):
        return "<{} name:'{}' image:{}>".format(type(self).__name__, self.name, self.image)