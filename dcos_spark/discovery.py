from __future__ import print_function
import os
import sys

import requests
import toml


def get_spark_task():
    dcos_config = os.getenv("DCOS_CONFIG")
    if dcos_config is None:
        print("Please specify DCOS_CONFIG env variable for reading DCOS "
              "config")
        sys.exit(1)

    with open(dcos_config) as f:
        config = toml.loads(f.read())

    marathon = config["marathon"]
    url = ("http://" + marathon["host"] + ":" + str(marathon["port"]) +
           "/v2/apps/spark")

    response = requests.get(url, timeout=5)

    if response.status_code >= 200:
        if 'app' not in response.json():
            print(response.json()['message'])
            sys.exit(1)

        return response.json()["app"]
    else:
        print("Bad response getting marathon app def. Status code: " +
              str(response.status_code))
        sys.exit(1)
        return ""


def get_spark_webui():
    spark_task = get_spark_task()
    tasks = spark_task['tasks']

    if len(tasks) == 0:
        print("Spark cluster task is not running yet.")
        sys.exit(1)

    return "http://" + tasks[0]["host"] + ":" + str(tasks[0]["ports"][1])


def get_spark_dispatcher():
    dcos_spark_url = os.getenv("DCOS_SPARK_URL")
    if dcos_spark_url is not None:
        return dcos_spark_url

    spark_task = get_spark_task()
    tasks = spark_task['tasks']

    if len(tasks) == 0:
        print("Spark cluster task is not running yet.")
        sys.exit(1)

    return tasks[0]["host"] + ":" + str(tasks[0]["ports"][0])
