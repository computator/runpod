from __future__ import absolute_import, print_function, unicode_literals
import pprint

CMD_HELP = {
        'dump': "dump the generated podspec to stdout for debugging"
    }

def get_cmd_names():
    return ('dump',)

def cmd_dump(podspec, opts):
    pprint.pprint(podspec)