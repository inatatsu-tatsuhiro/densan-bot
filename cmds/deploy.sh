#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE:-$0}"); pwd)

cd $SCRIPT_DIR/../
docker-compose down

git pull

docker-compose build

docker-compose up -d