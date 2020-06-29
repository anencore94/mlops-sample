#!/bin/bash

REPOSITORY_URL=localhost:5000
VERSION=v0.1.0
IMAGE_NAME=model-ae

docker build -t model-ae:$VERSION .
docker tag model-ae:$VERSION $REPOSITORY_URL/model-ae:$VERSION

docker push $REPOSITORY_URL/model-ae:$VERSION