from __future__ import print_function
import os
import sys

import requests
import toml


def get_arangodb_framework(name):
    dcos_config = os.getenv("DCOS_CONFIG")

    if dcos_config is None:
        print("Please specify DCOS_CONFIG env variable for reading DCOS "
              "config")
        sys.exit(1)

    with open(dcos_config) as f:
        config = toml.loads(f.read())

    if 'master' in config:
        master = config['master']
        url = ("http://" + master["host"] + ":" + str(master["port"]) + "/master/state.json")
    else:
        marathon = config['marathon']
        url = ("http://" + marathon["host"] + ":5050/master/state.json")

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        print("cannot connect to '" + url + "', please check your config")
        sys.exit(1)

    if response.status_code >= 200:
        json = response.json()

        if 'frameworks' not in json:
            print(json)
            sys.exit(1)

	frameworks = json['frameworks']

        for framework in frameworks:
            if name == framework['name']:
                return framework

        print("ArangoDB framework '" + name + "' is not running yet.")
        sys.exit(1)
    else:
        print("Bad response getting master state. Status code: " + str(response.status_code))
        sys.exit(1)


def get_arangodb_webui(name):
    if name == None:
	name = "arangodb-cluster"

    arangodb_framework = get_arangodb_framework(name)
    return arangodb_framework['webui_url']


def get_mode(name):
    url = get_arangodb_webui(name) + "v1/mode.json"
    response = requests.get(url, timeout=5)

    if response.status_code >= 200:
        json = response.json()
        return json["mode"]
    else:
        print("Bad response getting mode. Status code: " + str(response.status_code))
        sys.exit(1)


def destroy_cluster(name):
    url = get_arangodb_webui(name) + "v1/destroy.json"
    response = requests.post(url, timeout=5)

    if response.status_code >= 200:
        json = response.json()
        return json
    else:
        print("Bad response getting mode. Status code: " + str(response.status_code))
        sys.exit(1)
