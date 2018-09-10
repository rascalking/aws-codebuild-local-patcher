#!/bin/bash

set -e

virtualenv venv
pip install -r requirements.txt
./extract_file_from_image.py
patch < local_build.patch
docker build -t aws_codebuild_local:bugfix .
