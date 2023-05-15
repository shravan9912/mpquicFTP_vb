#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CONTAINER=${DIR##*/}

CONTAINERTAG=wuhongjia/rlmultipath # Modify to your own dockerhub user/repo

docker login && docker tag ${CONTAINER} ${CONTAINERTAG} && docker push ${CONTAINERTAG} && echo "Finished uploading ${CONTAINERTAG}"
