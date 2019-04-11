from __future__ import absolute_import, print_function, unicode_literals
import six
import yaml

from runpod.parsers import ParseError

def parse_file(src_file):
    try:
        data = yaml.safe_load(src_file)
    except yaml.YAMLError as e:
        six.raise_from(ParseError("YAML parse error: " + str(e)), e)
    if data is None:
        raise ParseError("File must not be empty")
    return parse_object(data)

def parse_object(data):
    return data