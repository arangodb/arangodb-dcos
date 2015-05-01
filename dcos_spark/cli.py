"""Run and manage Spark jobs

Usage:
    dcos spark --help
    dcos spark --info
    dcos spark --version
    dcos spark --config-schema
    dcos spark run --help
    dcos spark run --submit-args=<spark-args>
    dcos spark status <submissionId>
    dcos spark kill <submissionId>
    dcos spark webui

Options:
    --help                  Show this screen
    --info                  Show info
    --version               Show version
"""
from __future__ import print_function
import docopt
from dcos_spark import constants, discovery, spark_submit


def master():
    return discovery.get_spark_dispatcher()


def run_spark_job(args):
    return spark_submit.submit_job(master(), args['--submit-args'])

def show_spark_submit_help():
    return spark_submit.show_help()


def job_status(args):
    return spark_submit.job_status(master(), args['<submissionId>'])


def kill_job(args):
    return spark_submit.kill_job(master(), args['<submissionId>'])


def print_webui(args):
    print(discovery.get_spark_webui())
    return 0

def print_schema():
    print("{}")

def main():
    args = docopt.docopt(
        __doc__,
        version='dcos-spark version {}'.format(constants.version), help=False)

    if args['--info']:
        print(__doc__.split('\n')[0])
    elif args['--config-schema']:
        print_schema()
    elif args['run'] and args['--help']:
        return show_spark_submit_help()
    elif args['run']:
        return run_spark_job(args)
    elif args['status']:
        return job_status(args)
    elif args['kill']:
        return kill_job(args)
    elif args['webui']:
        return print_webui(args)
    else:
        print(__doc__)
        return 1

    return 0
