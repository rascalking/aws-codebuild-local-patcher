#!/bin/bash

set -e

virtualenv venv
pip install -r requirements.txt
./extract_file_from_image.py
chmod a+x ./local_build.sh
patch < local_build.patch
docker build -t aws-codebuild-local:bugfix .
