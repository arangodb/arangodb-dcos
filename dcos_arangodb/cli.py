"""Run and manage ArangoDB

Usage:
    dcos arangodb --help
    dcos arangodb --info
    dcos arangodb --version
    dcos arangodb --config
    dcos arangodb uninstall [--app-id <name>]
    dcos arangodb mode [--app-id <name>]
    dcos arangodb webui [--app-id <name>]

Options:
    -h, --help        Show this screen
    --version         Show the version
"""

from __future__ import print_function
import docopt
from dcos_arangodb import constants, discovery, arangodb_submit


def destroy_cluster(args):
    print(discovery.destroy_cluster(args['<name>']))
    return 0


def print_mode(args):
    print(discovery.get_mode(args['<name>']))
    return 0


def print_webui(args):
    print(discovery.get_arangodb_webui(args['<name>']))
    return 0

def print_schema(args):
    print("{}")
    return 0


def main():
    args = docopt.docopt(
        __doc__,
        version='dcos-arangodb version {}'.format(constants.version), help=False)

    if args['--info']:
        print(__doc__.split('\n')[0])
    elif args['--version']:
        print('dcos-arangodb version {}'.format(constants.version))
    elif args['--config']:
        print_schema(args)
    elif args['uninstall']:
        return destroy_cluster(args)
    elif args['mode']:
        return print_mode(args)
    elif args['webui']:
        return print_webui(args)
    else:
        print(__doc__)
        return 1

    return 0
