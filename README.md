ArangoDB subcommand for DCOS
============================

This repository contains a subcommand "arangodb" for the DCOS command
line tool for Mesosphere clusters. It builds on top of the ArangoDB
framework/service which can be found in

    https://github.com/ArangoDB/arangodb-mesos

and which is distributed in binary form as a Docker image

    arangodb/arangodb-mesos
    
which in turn is built using the `Dockerfile` in

    https://github.com/ArangoDB/arangodb-mesos-docker.

See the [README.md](https://github.com/ArangoDB/arangodb-mesos) in the
framework repository for details on how the framework scheduler is
configured.


Introduction
------------

ArangoDB is a distributed, multi-model database featuring JSON
documents, graphs and key/value pairs. It has a unifying query language
that allows to mix all three data models and supports joins and
transactions. As a distributed application, it is a very natural wish to
be able to deploy an ArangoDB cluster easily on an Apache Mesos cluster,
such that one can reap the benefits of better resource usage that Mesos
promises, and run ArangoDB alongside other distributed applications.
This framework makes this wish come true.

An ArangoDB cluster consists of different processes. As a central
fault-tolerant configuration store we use `etcd`, we call these
processes "agents" and the whole `etcd`-cluster "agency". Usually one
will deploy three agents to allow for a failure (or indeed upgrade) of
one of them without service interruption. The second type of processes
are the "DBservers", which are ArangoDB instances that actually store
data. No client should ever (need to) contact the DBservers directly.
The third type of processes are the "coordinators". They are
ArangoDB instances as well, they are the ones that receive client
requests, export the usual ArangoDB HTTP/REST API, know the structure of
the ArangoDB cluster (via the agency), and organise the distribution
of the queries to the actual DBservers.

The user does not actually have to know much about this structure,
however, since one can scale the coordinator layer independently from
the DBserver layer, it is useful to understand this structure. As a rule
of thumb, scale the DBserver layer up to get more storage space and
scale the coordinator layer up if the bottleneck is CPU power for
queries or Foxx apps (which run on the coordinators).


Installation/Startup
--------------------

This assumes that you have a working Mesosphere cluster and `dcos` command
line utility. Deploying an ArangoDB cluster is easy, just do:

    dcos package update
    dcos package install arangodb

This will install the dcos subcommand and start an instance of the
ArangoDB framework/service under its standard name "arangodb" via
Marathon. If you only want to install the command line tool, use

    dcos package install --cli arangodb

For further configuration options using a JSON file see below in Section
"Configuration options". In particular the needed resources and the size
of the ArangoDB cluster can be configured in this way.


Deinstallation/Shutdown
-----------------------

To shutdown and delete your ArangoDB framework/service and to remove the
command line tool, do the following two commands:

    dcos arangodb uninstall ; dcos package uninstall arangodb

The first one uses the "arangodb" subcommand to gracefully shut down and
delete all instances of your ArangoDB service. The framework scheduler
itself will run in a silent mode for another 120 seconds. This enables
the second command to remove the "arangodb" subcommand and the entry in
Marathon that would otherwise restart the framework scheduler
automatically.


Changing the ArangoDB cluster at runtime
----------------------------------------

This is not yet implemented. You will be able to scale up and down the
ArangoDB cluster. The dcos subcommand will talk to the framework scheduler
over its HTTP/REST API.


Service discovery with Mesos-DNS
--------------------------------

All services started by the ArangoDB service are announced to Mesos and 
are thus available through Mesos-DNS, if you have it configured. The
most important ones are the coordinators, which are the processes with
which clients of the database cluster talk. The coordinators are called
"coordinator1" to "coordinatorX" where "X" is replaced with the total
number of coordinators. They all have a DNS entry in Mesos-DNS of the
form

    coordinator1.arangodb.mesos

which points to an IP address that is valid within the Mesos cluster. 
If you need to contact them from the outside you need some IP forwarding
rules. Furthermore, they all have an SRV record under a name like

    _coordinator1._tcp.arangodb.mesos

which contains a value like

    0 0 15639 coordinator1-26922-s0.arangodb.mesos.

Here, the number 15639 is the port number under which the corresponding
coordinator is reachable. There are similar entries for DBservers and
agents but you should not need them at all. All interaction with the
ArangoDB cluster goes via the coordinators.


Configuration options
---------------------

There are a number of options, which can be specified in the following
way:

    dcos package install --config=<JSON_FILE> arangodb

where `JSON_FILE` is the path to a JSON file. The following
attributes on the top level of this file are defined:

  - `arangodb/id`: a string, unique ID for the started cluster, do not
    confuse with --app-id, unfortunately, the two are not the same!

  - `arangodb/mode`: this must be a string and the possible values
    are "standalone" and "cluster". The former starts a fixed number of
    independent single server instances in the cluster. The latter starts
    a proper distributed ArangoDB cluster. This is the default.

  - `arangodb/minimum-resources-agent`: Mesos resource specification,
    one must specify `cpus`, `mem` and `disk`. Otherwise offers with zero
    values are accepted.

  - `arangodb/minimum-resources-dbserver`: Mesos resource specification,
    one must specify `cpus`, `mem` and `disk`. Otherwise offers with zero
    values are accepted. - `minimum-resources-coordinator`: Mesos resource
    specification, one must specify `cpus`, `mem` and `disk`. Otherwise
    offers with zero values are accepted.

  - `arangodb/nr-agents`: an integer, number of agent processes in the
    agency. Currently limited to 1.

  - `arangodb/nr-dbservers`: an integer, number of DBserver processes in
    the cluster.

  - `arangodb/nr-coordinators`: an integer, number of coordinator
    processes in the cluster.


Running more than one ArangoDB cluster on the same Mesosphere cluster
---------------------------------------------------------------------

If you want to run more than one instance of the ArangoDB service on
the same Mesosphere cluster, you have to specify `--app-id <name>` in
the `dcos package install` command as well as the configuration option
`arangodb/id`. They can be the same but need not be. Thus, start a new
cluster with

    dcos package install --config=myconfig.json --app-id=name1 arangodb

where `myconfig.json` is

    { "arangodb/id": "id1" }

Note the difference between "name1" and "id1"!

To destroy that cluster use

    dcos arangodb uninstall --app-id id1 ; dcos package uninstall arangodb --app-id name1

After this the `arangodb` subcommand will also be installed, to restore, do

    dcos package install --cli arangodb

This will give you access to your other running ArangoDB clusters.

Ideally, the additional option should be unnecessary, but currently this
trick is needed.


Support and bug reports
-----------------------

The ArangoDB Mesos framework as well as the DCOS subcommand are
supported by ArangoDB GmbH, the company behind ArangoDB. If you get
stuck, need help or have questions, just ask via one of the following
channels:

  - [Google Group](https://groups.google.com/forum/#!forum/arangodb)
  - `hackers@arangodb.com`: developer mailing list of ArangoDB
  - `max@arangodb.com`: direct email to Max Neunhöffer
  - `frank@arangodb.com`: direct email to Frank Celler

Additionally, we track issues, bug reports and questions via the github
issue trackers at

  - [arangodb-dcos](https://github.com/ArangoDB/arangodb-dcos/issues):
    the DCOS subcommand
  - [arangodb-mesos](https://github.com/arangodb/arangodb-mesos/issues):
    the ArangoDB framework/service

