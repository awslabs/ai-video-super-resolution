#!/bin/bash
# This assumes all of the OS-level configuration has been completed and git repo has already been cloned
#
# This script should be run from the repo's deployment directory
# cd deployment
# ./build-s3-dist.sh
#
# Check to see if input has been provided:
# if [ "$1" ]; then
#     echo "Usage: ./build-s3-dist.sh"
#     exit 1
# fi

set -e

title() {
    echo "------------------------------------------------------------------------------"
    echo $*
    echo "------------------------------------------------------------------------------"
}

run() {
    >&2 echo ::$*
    $*
}

# Get reference for all important folders
template_dir="$PWD"

echo "------------------------------------------------------------------------------"
echo "cdk synth"
echo "------------------------------------------------------------------------------"
cd ${template_dir}
__dir="$(cd "$(dirname $0)";pwd)"
CDK_OUT_PATH="${__dir}/../cdk.out"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Parameters not enough"
    echo "Example: $(basename $0) <BUCKET_NAME> <SOLUTION_NAME> [VERSION]"
    exit 1
fi

export BUCKET_NAME=$1
export SOLUTION_NAME=$2
export GLOBAL_S3_ASSETS_PATH="${__dir}/global-s3-assets"
export REGIONAL_S3_ASSETS_PATH="${__dir}/regional-s3-assets"

echo "------------------------------------------------------------------------------"
echo "init env"
echo "------------------------------------------------------------------------------"
title "init env"

run rm -rf ${GLOBAL_S3_ASSETS_PATH} && run mkdir -p ${GLOBAL_S3_ASSETS_PATH}
run rm -rf ${REGIONAL_S3_ASSETS_PATH} && run mkdir -p ${REGIONAL_S3_ASSETS_PATH}
run rm -rf ${CDK_OUT_PATH}

if [ -z "$3" ]; then
    export VERSION=$(git describe --tags || echo latest)
    echo "BUCKET_NAME=${BUCKET_NAME}"
    echo "SOLUTION_NAME=${SOLUTION_NAME}"
    echo "VERSION=${VERSION}"

else
    export VERSION=$3
fi

echo "${VERSION}" > ${GLOBAL_S3_ASSETS_PATH}/version

# cd ..
# pip install -r requirements.txt
# cd layers
# chmod +x build_layer.sh
# ./build_layer.sh

cd ..
run npm install -g aws-cdk

export USE_BSS=true
# How to config https://github.com/wchaws/cdk-bootstrapless-synthesizer/blob/main/API.md
export BSS_TEMPLATE_BUCKET_NAME="${BUCKET_NAME}"
export BSS_FILE_ASSET_BUCKET_NAME="${BUCKET_NAME}-\${AWS::Region}"
export BSS_FILE_ASSET_PREFIX="${SOLUTION_NAME}/${VERSION}/"
export BSS_FILE_ASSET_REGION_SET="us-east-1,${BSS_FILE_ASSET_REGION_SET}"

cdk synth -c inferentia=true --output ${CDK_OUT_PATH}

echo "${VERSION}" > ${GLOBAL_S3_ASSETS_PATH}/version
run ${__dir}/helper.py ${CDK_OUT_PATH}
cp -r deployment/ ../../deployment/
