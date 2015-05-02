from __future__ import print_function
import os
import toml


def dcos_config():
    config_file = os.getenv('DCOS_CONFIG')
    with open(config_file) as data_file:
        data = toml.loads(data_file.read())
    return data


def marathon_uri():
    config = dcos_config()
    return config
