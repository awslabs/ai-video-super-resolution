import ffmpeg
import boto3
import os
import re
import glob
import math
import subprocess
from urllib.parse import unquote_plus
from botocore.config import Config
import json

s3_client = boto3.client('s3', os.environ['AWS_REGION'], config=Config(s3={'addressing_style': 'path'}, user_agent_extra=os.environ['user_agent_extra']))
efs_path = os.environ['EFS_PATH']
parallel_groups = int(os.environ['PARALLEL_GROUPS'])

def slice_video(key):
    segment_prefix, segment_ext = os.path.splitext(os.path.basename(key))
    segment_filename = segment_prefix + '.%03d' + segment_ext
    s3_client.download_file(os.environ['S3_BUCKET'], key, f'{efs_path}/{key}')

    try:
        probe = ffmpeg.probe(f'{efs_path}/{key}')
    except Exception as e:
        print(e.stderr.decode('utf8'))
    
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    
    if 'duration' in video_stream:
        duration = video_stream['duration']
    else:
        duration = probe['format']['duration']
    segment_num = min(math.ceil(float(duration)/60), 1000)
    segment_time = math.ceil(float(duration)/segment_num)
    segment_files = glob.glob(os.path.join(efs_path, segment_prefix) + '_seg_[0-9][0-9][0-9]'+ segment_ext)
    os.remove(f'{efs_path}/{key}')
    for file in segment_files:
        os.remove(file)
    return segment_num

def handler(event, context):
    if isinstance(event['body'], str):
        body = json.loads(event['body'])
    else:
        body = event['body']
    key = body['key']
    task = body.get('task', 'inference')
    scale = body.get('scale', '2')
    env = body.get('env', 'spot')
    if env == 'onDemand':
        env = 'SuperResolution_queue_onDemand'
    else:
        env = 'SuperResolution_queue_Spot'
    batchClient = boto3.client('batch')
    if task == 'debug':
        response = batchClient.submit_job(
            jobName=key.replace('.','_') + "-debug",
            jobQueue=env,
            jobDefinition='SuperResolution',
            parameters={
                'File': key,
                'Scale': scale,
                'TaskFlag': 'debug'
            },
        )
        return {"statusCode": 200, "body": key + " debug"}
    video_segments_num = slice_video(key)
    response = batchClient.submit_job(
        jobName=key.replace('.','_') + "-Split",
        jobQueue=env,
        jobDefinition='SuperResolution',
        parameters={
            'File': key,
            'Scale': scale,
            'TaskFlag': 'split'
        },
    )
    if video_segments_num<=1:
        response = batchClient.submit_job(
            jobName=key.replace('.','_') + "-SR",
            jobQueue=env,
            jobDefinition='SuperResolution',
            dependsOn=list(map(lambda id: {
                'jobId': id,
                'type': 'N_TO_N'
            }, [response['jobId']])),
            parameters={
                'File': key,
                'Scale': scale,
                'TaskFlag': 'inference'
            },
        )
    else:
        response = batchClient.submit_job(
            jobName=key.replace('.','_') + "-SR",
            jobQueue=env,
            arrayProperties={
                'size': video_segments_num
            },
            jobDefinition='SuperResolution',
            dependsOn=list(map(lambda id: {
                'jobId': id,
                'type': 'N_TO_N'
            }, [response['jobId']])),
            parameters={
                'File': key,
                'Scale': scale,
                'TaskFlag': 'inference'
            },
        )
    response = batchClient.submit_job(
        jobName=key.replace('.','_') + "-Consolidation",
        jobQueue=env,
        jobDefinition='SuperResolution',
        dependsOn=list(map(lambda id: {
                'jobId': id,
                'type': 'SEQUENTIAL'
            }, [response['jobId']])),
        parameters={
            'File': key,
            'Scale': scale,
            'TaskFlag': 'merge'
        },
    )
    return {
       "statusCode": 200,
       "body": key + " started"}
