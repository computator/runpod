from __future__ import absolute_import, print_function, unicode_literals
import pkgutil

__path__ = pkgutil.extend_path(__path__, __name__)

class ParseError(Exception):
    pass