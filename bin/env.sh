#!/bin/bash -e

BASEDIR=`dirname $0`/..

if [ ! -d "$BASEDIR/env" ]; then
    virtualenv -q $BASEDIR/env --prompt='(dcos-spark) '
    echo "Virtualenv created."
fi

cd $BASEDIR
source $BASEDIR/env/bin/activate
echo "Virtualenv activated."

if [ ! -f "$BASEDIR/env/updated" -o $BASEDIR/setup.py -nt $BASEDIR/env/updated ]; then
    pip install -e $BASEDIR
    touch $BASEDIR/env/updated
    echo "Requirements installed."
fi

pip install -r $BASEDIR/requirements.txt

if [ ! -d "$BASEDIR/dcos_spark/data/spark*" ]; then
    pushd .
    cd $BASEDIR/dcos_spark/data
    wget http://downloads.mesosphere.com.s3.amazonaws.com/assets/spark/spark-1.4.0-SNAPSHOT-bin-2.2.0.tgz
    tar xvf spark-1.4.0-SNAPSHOT-bin-2.2.0.tgz
    rm spark-1.4.0-SNAPSHOT-bin-2.2.0.tgz
    popd
fi
