#!/bin/bash

wget https://raw.githubusercontent.com/aws/aws-codebuild-docker-images/master/local_builds/codebuild_build.sh
patch < codebuild_build.patch
chmod a+x ./codebuild_build.sh
