#!/bin/bash
set -euo pipefail
set -o errexit
set -o errtrace
IFS=$'\n\t'

# Configuring temporary path for caching or streaming
# finally we create an empty directory for mounting the blob container (/root/azure-storage)
mkdir -p /mnt/resource/blobfusetmp \
    && chown root /mnt/resource/blobfusetmp \
    && mkdir -p /mnt/containermnt

# Authorize access to your storage account and mount our blobstore
# Example: https://github.com/Azure/azure-storage-fuse/blob/main/sampleFileCacheConfig.yaml
# Full Config: https://github.com/Azure/azure-storage-fuse/blob/main/setup/baseConfig.yaml
blobfuse2 mount /mnt/containermnt --config-file=/home/ibf/fuse_connection_510datalake.yaml

# run the command passed to us
exec "$@"