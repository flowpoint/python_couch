#!/bin/bash
podman run -d -p 8001:5984 --name couchdb -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=temppwd apache/couchdb:latest
