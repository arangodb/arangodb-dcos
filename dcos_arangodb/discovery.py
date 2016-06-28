from __future__ import print_function

import os
import sys

from dcos import http, config
import toml

from dcos.errors import DCOSException

def get_arangodb_framework(name):
    url = config.get_config_val('core.dcos_url') + "/mesos/state.json"
    try:
        response = http.get(url, timeout=15)
    except DCOSException as e:
        print("cannot connect to '" + url + "'", e)
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
        service_url = arangodb_framework['webui_url'].rstrip("/")
    else:
        base_url = config.get_config_val('core.dcos_url').rstrip("/")
        service_url = base_url + "/service/" + name

    
    # find out if arangodb is mounted (new world) or if the framework is mounted
    version_url = service_url + "/_db/_system/_api/version"

    try:
        response = http.get(version_url, timeout=15)
    except DCOSException as e:
        # mop: as far as I get it I can't access the original http response because a completely new
        # exception has been raised. what I would want to check is if there is a 404 which would
        # indicate that this is an "old" version of the framework
        return service_url

    return service_url + "/framework"

def get_mode(name, internal):
    url = get_arangodb_webui(name, internal) + "/v1/mode.json"

    try:
        response = http.get(url, timeout=15)
    except DCOSException as e:
        print("cannot connect to '" + url + "'", e)
        sys.exit(1)

    if response.status_code >= 200 and response.status_code < 300:
        json = response.json()
        return json["mode"]
    else:
        print("Bad response getting mode. Status code: "
              + str(response.status_code))
        sys.exit(1)

def get_endpoints_coordinators(name, internal):
    url = get_arangodb_webui(name, internal) + "/v1/endpoints.json"

    try:
        response = http.get(url, timeout=15)
    except DCOSException as e:
        print("cannot connect to '" + url + "'", e)
        sys.exit(1)

    if response.status_code >= 200 and response.status_code < 300:
        json = response.json()
        return json["coordinators"]
    else:
        print("Bad response getting endpoints. Status code: "
              + str(response.status_code))
        sys.exit(1)

def get_endpoints_dbservers(name, internal):
    url = get_arangodb_webui(name, internal) + "/v1/endpoints.json"

    try:
        response = http.get(url, timeout=15)
    except DCOSException as e:
        print("cannot connect to '" + url + "'", e)
        sys.exit(1)

    if response.status_code >= 200 and response.status_code < 300:
        json = response.json()
        return json["dbservers"]
    else:
        print("Bad response getting endpoints. Status code: "
                + str(response.status_code))
        sys.exit(1)



def destroy_cluster(name, internal):
    url = get_arangodb_webui(name, internal) + "/v1/destroy.json"

    try:
        response = http.post(url, timeout=60)
    except DCOSException as e:
        print("cannot connect to '" + url + "'", e)
        sys.exit(1)

    if response.status_code >= 200 and response.status_code < 300:
        json = response.json()
        return json
    else:
        print("Bad response getting mode. Status code: "
                + str(response.status_code))
        sys.exit(1)
