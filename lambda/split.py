import ffmpeg
import boto3
import os
import re
import math
from botocore.config import Config
import json

s3_client = boto3.client('s3', os.environ['AWS_REGION'], config=Config(s3={'addressing_style': 'path'}, user_agent_extra=os.environ['user_agent_extra']))
efs_path = os.environ['EFS_PATH']
instance_types = os.environ['instance_types']
parallel_groups = int(os.environ['PARALLEL_GROUPS'])

def slice_video(key, segment_time, scale):
    key_store = key.replace('/','#')
    try:
        presigned_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': os.environ['S3_BUCKET'], 'Key': key}, ExpiresIn=1000)
        probe = ffmpeg.probe(presigned_url)
    except Exception as e:
        print(e.stderr.decode('utf8'))
        s3_client.download_file(os.environ['S3_BUCKET'], key, f'{efs_path}/{key_store}')
        probe = ffmpeg.probe(f'{efs_path}/{key_store}')
        print('finished download video')
    print('probe video info')
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if instance_types == 'inf1.xlarge':
        if video_stream['height']*video_stream['width']*scale*scale > 3840*2160:
            return -1

    if 'duration' in video_stream:
        duration = video_stream['duration']
    else:
        duration = probe['format']['duration']
    segment_num = math.ceil(float(duration)/int(segment_time))
    return segment_num

def handler(event, context):
    if isinstance(event['body'], str):
        body = json.loads(event['body'])
    else:
        body = event['body']
    key = body['key']
    task = body.get('task', 'inference')
    scale = str(body.get('scale', '2'))
    env = body.get('env', 'spot')
    job_name = re.sub(r'[^A-Za-z0-9_-]', '-' , key)
    segment_time = body.get('segment_time', '60')
    if env == 'onDemand':
        env = 'SuperResolution_queue_onDemand'
    else:
        env = 'SuperResolution_queue_Spot'
    batchClient = boto3.client('batch')
    if task == 'debug':
        response = batchClient.submit_job(
            jobName=job_name + "-debug",
            jobQueue=env,
            jobDefinition='SuperResolution',
            parameters={
                'File': key,
                'Scale': scale,
                'SegmentTime': segment_time,
                'TaskFlag': 'debug'
            },
        )
        return {"statusCode": 200, "body": key + " debug"}
    video_segments_num = slice_video(key, segment_time, int(scale))
    key_store = key.replace('/','#')
    if video_segments_num == -1:
        return {
            "statusCode": 400,
            "body": "Video size exceeded the limit"}
    response = batchClient.submit_job(
        jobName=job_name + "-Split",
        jobQueue=env,
        jobDefinition='SuperResolution',
        parameters={
            'File': key_store,
            'Scale': scale,
            'SegmentTime': segment_time,
            'TaskFlag': 'split'
        },
    )
    if video_segments_num<=1:
        response = batchClient.submit_job(
            jobName=job_name + "-SR",
            jobQueue=env,
            jobDefinition='SuperResolution',
            dependsOn=[{
                'jobId': response['jobId']
            }],
            parameters={
                'File': key_store,
                'Scale': scale,
                'SegmentTime': segment_time,
                'TaskFlag': 'inference'
            },
        )
    else:
        response = batchClient.submit_job(
            jobName=job_name + "-SR",
            jobQueue=env,
            arrayProperties={
                'size': video_segments_num
            },
            jobDefinition='SuperResolution',
            dependsOn=[{
                'jobId': response['jobId']
            }],
            parameters={
                'File': key_store,
                'Scale': scale,
                'SegmentTime': segment_time,
                'TaskFlag': 'inference'
            },
        )
    #return job id for SR job , added by zhuyao
    SR_Job=response['jobId']

    response = batchClient.submit_job(
        jobName=job_name + "-Merge",
        jobQueue=env,
        jobDefinition='SuperResolution',
        dependsOn=list(map(lambda id: {
                'jobId': id,
                'type': 'SEQUENTIAL'
            }, [response['jobId']])),
        parameters={
            'File': key_store,
            'Scale': scale,
            'SegmentTime': segment_time,
            'TaskFlag': 'merge'
        },
    )
    return {
       "statusCode": 200,
       "body": key + " started, SuperResolution Job Id is: #" + SR_Job +'#'}
