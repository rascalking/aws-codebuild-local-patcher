#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import tarfile
import tempfile

import docker


def main():
    args = parse_args()
    client = docker.from_env()
    image = client.images.pull(args.source_image)
    path = args.path.lstrip('/') # image tarballs are relative to /

    # get a tarfile of the image
    saved_image_fh = tempfile.TemporaryFile()
    for chunk in image.save():
        saved_image_fh.write(chunk)
    saved_image_fh.seek(0)
    image_tarfile = tarfile.open(fileobj=saved_image_fh)

    # load up the image manifest
    try:
        image_manifest = json.load(image_tarfile.extractfile('manifest.json'))
    except KeyError:
        print('Unable to find manifest.json in docker save output, contents are:')
        image_tarfile.list()
        return 1

    # look for your path in the topmost layer it can be found in
    for layer_tar_name in reversed(image_manifest[0]['Layers']):
        layer_tarfile_fh = image_tarfile.extractfile(layer_tar_name)
        layer_tarfile = tarfile.open(fileobj=layer_tarfile_fh)

        # check if your path is in this layer
        try:
            tar_info = layer_tarfile.getmember(path)
        except KeyError:
            continue

        # copy it out of the layer's tarfile
        with layer_tarfile.extractfile(path) as source:
            with open(os.path.basename(path), 'w+b') as destination:
                chunk = source.read()
                while chunk:
                    # TODO: proper amounts of paranoia around write
                    destination.write(chunk)
                    chunk = source.read()
        return 0
    print('Unable to find path {} in image {}'.format(args.path, args.source_image))
    return 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-image', default='amazon/aws-codebuild-local:latest')
    parser.add_argument('--path', default='/usr/local/bin/local_build.sh')
    return parser.parse_args()


if __name__ == '__main__':
    raise SystemExit(main())
