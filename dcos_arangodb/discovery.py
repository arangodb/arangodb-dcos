from __future__ import print_function

import os
import sys

import requests
import toml

from dcos import util

def get_arangodb_framework(name):
    url = util.get_config().get('core.dcos_url') + ":5050/master/state.json"
    try:
        response = requests.get(url, timeout=15)
    except requests.exceptions.ConnectionError:
        print("cannot connect to '" + url + "', please check your config")
        sys.exit(1)

    if response.status_code >= 200 and response.status_code < 300:
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
        print("Bad response getting master state. Status code: "
              + str(response.status_code))
        sys.exit(1)


def get_arangodb_webui(name, internal):
    if name is None:
        name = "arangodb"

    if internal:
        arangodb_framework = get_arangodb_framework(name)
        return arangodb_framework['webui_url']
    else:
        base_url = util.get_config().get('core.dcos_url').rstrip("/")
        return base_url + "/service/" + name


def get_mode(name, internal):
    url = get_arangodb_webui(name, internal) + "/v1/mode.json"

    try:
        response = requests.get(url, timeout=15)
    except requests.exceptions.ConnectionError:
        print("cannot connect to '" + url
              + "', please check that the ArangoDB framework is running")
        sys.exit(1)
    except requests.exceptions.ConnectTimeout:
        print("cannot connect to '" + url + "', please check your network")
        sys.exit(1)

    if response.status_code >= 200 and response.status_code < 300:
        json = response.json()
        return json["mode"]
    else:
        print("Bad response getting mode. Status code: "
              + str(response.status_code))
        sys.exit(1)


def destroy_cluster(name, internal):
    url = get_arangodb_webui(name, internal) + "/v1/destroy.json"

    try:
        response = requests.post(url, timeout=60)
    except requests.exceptions.ConnectionError:
        print("cannot connect to '" + url
              + "', please check that the ArangoDB framework is running")
        sys.exit(1)
    except requests.exceptions.ConnectTimeout:
        print("cannot connect to '" + url + "', please check your network")
        sys.exit(1)

    if response.status_code >= 200 and response.status_code < 300:
        json = response.json()
        return json
    else:
        print("Bad response getting mode. Status code: "
              + str(response.status_code))
        sys.exit(1)
