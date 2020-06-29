#!/bin/bash

REPOSITORY_URL=localhost:5000
VERSION=v0.1.2

docker build -t hello-flask:$VERSION .
docker tag hello-flask:$VERSION $REPOSITORY_URL/hello-flask:$VERSION

docker push $REPOSITORY_URL/hello-flask:$VERSION