#!/usr/bin/env bash

docker build -t ffmpeg_layer .
docker run --rm -v $(pwd):/data ffmpeg_layer cp /packages/ffprobe.zip /data
docker rmi ffmpeg_layer



