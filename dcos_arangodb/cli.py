"""Run and manage ArangoDB

Usage:
    dcos arangodb --help
    dcos arangodb --info
    dcos arangodb --version
    dcos arangodb --config-schema
    dcos arangodb uninstall [--app-id <name>] [--internal]
    dcos arangodb mode [--app-id <name>] [--internal]
    dcos arangodb webui [--app-id <name>] [--internal]

Options:
    -h, --help        Show this screen
    --version         Show the version
"""

from __future__ import print_function

import docopt
from dcos_arangodb import constants, discovery


def destroy_cluster(args, internal):
    print(discovery.destroy_cluster(args['<name>'], internal))
    return 0


def print_mode(args, internal):
    print(discovery.get_mode(args['<name>'], internal))
    return 0


def print_webui(args, internal):
    print(discovery.get_arangodb_webui(args['<name>'], internal))
    return 0


def print_schema(args):
    print("{}")
    return 0


def main():
    args = docopt.docopt(
        __doc__,
        version='dcos-arangodb version {}'.format(constants.version),
        help=False)

    internal = False

    if args['--internal']:
        internal = True

    if args['--info']:
        print(__doc__.split('\n')[0])
    elif args['--help']:
        print(__doc__)
    elif args['--version']:
        print('dcos-arangodb version {}'.format(constants.version))
    elif args['--config-schema']:
        print_schema(args)
    elif args['uninstall']:
        return destroy_cluster(args, internal)
    elif args['mode']:
        return print_mode(args, internal)
    elif args['webui']:
        return print_webui(args, internal)
    else:
        print(__doc__)
        return 1

    return 0
