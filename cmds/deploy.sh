#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE:-$0}"); pwd)

docker-compose down

git pull

docker-compose build

docker-compose up -d