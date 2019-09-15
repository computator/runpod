from __future__ import absolute_import, print_function, unicode_literals
import six
import yaml

from runpod.parsers import ParseError

DEFAULT_FILENAME = 'kubernetes.yaml'

def parse_file(src_file):
    try:
        data = list(yaml.safe_load_all(src_file))
    except yaml.YAMLError as e:
        six.raise_from(ParseError("YAML parse error: " + str(e)), e)
    if len(data) == 0:
        raise ParseError("File must not be empty")
    if any(True for doc in data if doc is None):
        raise ParseError("Empty YAML documents are not allowed")
    return parse_object(data)

def parse_object(data):
    return data