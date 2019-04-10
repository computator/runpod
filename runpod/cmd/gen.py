from __future__ import absolute_import, print_function, unicode_literals

def get_cmd_names():
    return ('gen',)

def init_cmd_subparsers(add_parser):
    parser = add_parser("gen")
    parser.add_argument('gen_format', choices=("systemd",))

def cmd_gen(podspec, opts):
    print(podspec, opts)