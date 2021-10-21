#!/usr/bin/env bash
wget --no-check-certificate https://xiaotih.s3.us-west-2.amazonaws.com/ffprobe.zip -O $(pwd)/ffprobe.zip
#docker build -t ffmpeg_layer .
#docker run --rm -v $(pwd):/data ffmpeg_layer cp /packages/ffprobe.zip /data
#docker rmi ffmpeg_layer



