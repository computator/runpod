from __future__ import absolute_import, print_function, unicode_literals

CMD_HELP = {
        'gen': "generate service config files for a pod"
    }

def get_cmd_names():
    return ('gen',)

def init_cmd_subparsers(add_parser):
    parser = add_parser("gen", help=CMD_HELP['gen'])
    parser.add_argument('gen_format', choices=("systemd",), help="set the output format for the service file(s)")

def cmd_gen(podspec, opts):
    print(podspec, opts)