"""Run and manage Spark jobs

Usage:
    dcos arangodb --help
    dcos arangodb --info
    dcos arangodb --version
    dcos arangodb --config-schema
    dcos arangodb webui [--app-id <name>]

Options:
    --help                  Show this screen
    --info                  Show info
    --version               Show version
"""
from __future__ import print_function
import docopt
from dcos_arangodb import constants, discovery, arangodb_submit


def master():
    return discovery.get_arangodb_dispatcher()


def run_arangodb_job(args):
    return arangodb_submit.submit_job(master(), args['--submit-args'])

def show_arangodb_submit_help():
    return arangodb_submit.show_help()


def job_status(args):
    return arangodb_submit.job_status(master(), args['<submissionId>'])


def kill_job(args):
    return arangodb_submit.kill_job(master(), args['<submissionId>'])


def print_webui(args):
    print(discovery.get_arangodb_webui(args['<name>']))
    return 0

def main():
    args = docopt.docopt(
        __doc__,
        version='dcos-arangodb version {}'.format(constants.version), help=False)

    if args['--info']:
        print(__doc__.split('\n')[0])
    elif args['webui']:
        return print_webui(args)
    else:
        print(__doc__)
        return 1

    return 0
