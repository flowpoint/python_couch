#!/bin/bash
docker run -d -p 8001:5984 --rm --name couchdb -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=temppwd apache/couchdb:latest
