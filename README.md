# aws-codebuild-local-patcher

Builds a patched `amazon/aws-codebuild-local` image, and a patched
`codebuild_build.sh` script that references it.

Assumptions:
* python3 with virtualenv and pip
* sudoless access to docker
* wget


```
$ build_patched_aws_codebuild_local.sh
$ build_patched_codebuild_build.sh
```
