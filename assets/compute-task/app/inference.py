import argparse
import cv2
import ffmpeg
from fractions import Fraction
import logging
import numpy as np
import os
import torch
import torch.neuron
from tqdm import tqdm
import utils

logging.basicConfig(level=logging.DEBUG)

if 'AWS_BATCH_JOB_ARRAY_INDEX' not in os.environ:
    os.environ['AWS_BATCH_JOB_ARRAY_INDEX'] = '0'
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--method', default='BSR', choices=['BSR'])
parser.add_argument('-i', '--input', required=True)
parser.add_argument('-s', '--scale', default=2)
args = parser.parse_args()
scale = int(args.scale)

if False:
    import glob
    import boto3
    segment_prefix, segment_ext = os.path.splitext(os.path.basename(args.input))
    segment_filename = segment_prefix + '_seg_[0-9][0-9][0-9]_{}{}'.format(args.method, segment_ext)
    video_file = os.path.join('/input', segment_filename)
    filie_list_hr = glob.glob(video_file)
    filie_list_hr.sort()
    segment_prefix, segment_ext = os.path.splitext(os.path.basename(args.input))
    segment_filename = segment_prefix + '_seg_[0-9][0-9][0-9]' + segment_ext
    bucket = boto3.resource('s3', region_name=os.environ['AWS_REGION']).Bucket(os.environ['S3_BUCKET']) 
    filie_list_lr = glob.glob(os.path.join('/input', segment_filename))
    for segment in filie_list_hr + filie_list_lr:
        bucket.upload_file(segment, os.path.join(f'{segment_prefix}_{segment_ext[1:]}_debug', os.path.basename(segment)))
    exit()
    
if False:
    import glob
    import subprocess
    import boto3
    segment_prefix, segment_ext = os.path.splitext(os.path.basename(args.input))
    segment_filename = segment_prefix + '_seg_[0-9][0-9][0-9]_{}{}'.format(args.method, segment_ext)
    video_file = os.path.join('/input', segment_filename)
    video_file_list = glob.glob(video_file)
    video_file_list.sort()
    with open(video_file + ".txt", "w") as f:
        for segment in video_file_list:
            f.write('file {} \n'.format(segment))
    
    cmd = ['ffmpeg', '-f', 'concat', '-safe',
           '0', '-i', video_file + ".txt", '-c', 'copy', os.path.join('/input', segment_prefix + '_' + args.method + segment_ext), '-y']
    print("merge video segments ....")
    subprocess.call(cmd)
    os.remove(video_file + ".txt")
    bucket = boto3.resource('s3', region_name=os.environ['AWS_REGION']).Bucket(os.environ['S3_BUCKET']) 
    bucket.upload_file(os.path.join('/input', segment_prefix + '_' + args.method + segment_ext), segment_prefix + '_' + args.method + segment_ext)
    os.remove(os.path.join('/input', segment_prefix + '_' + args.method + segment_ext))
    for segment in video_file_list:
        os.remove(segment)
    exit()
    
segment_prefix, segment_ext = os.path.splitext(os.path.basename(args.input))
segment_filename = segment_prefix + '.{0:03d}'.format(int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])) + segment_ext
logging.info(f'Processing {segment_filename} ...')

video_file = os.path.join('/input', segment_filename)
fname, ext = os.path.splitext(os.path.basename(video_file))

           
try:
    probe = ffmpeg.probe(video_file, loglevel = 56)
except Exception as e:
    logging.error(e.stderr.decode('utf8'))
    raise e
    
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
if len([stream for stream in probe['streams'] if stream['codec_type'] == 'audio']) == 0:
    audio_enable = False
else:
    audio = ffmpeg.input(video_file).audio
    audio_enable = True
width = int(video_stream['width'])
height = int(video_stream['height'])
avg_frame_rate = round(Fraction(video_stream['avg_frame_rate']))
img_shape = (height, width)
max_len =  utils.get_nb_frames(video_file, width, height, avg_frame_rate)
method = args.method

class GANInference():
    def __init__(self, img_shape, scale, model_shape=(72, 72), shave=10, method='BSR'):
        
        self.scale = scale
        self.ori_shape = img_shape
        self.input_shape = (img_shape[0]//(model_shape[0]-shave)*(model_shape[0]-shave) + model_shape[0],
                            img_shape[1]//(model_shape[1]-shave)*(model_shape[1]-shave) + model_shape[1])
        self.output_shape = (self.input_shape[0]*scale, self.input_shape[1]*scale)
        self.patches = []
        for i in range(0, img_shape[0], model_shape[0]-shave):
            for j in range(0, img_shape[1], model_shape[1]-shave):
                self.patches.append((slice(i, i+model_shape[0]), slice(j, j+model_shape[1])))
        self.pad_top = (self.input_shape[0] - img_shape[0])//2
        self.pad_bottom = self.input_shape[0] - img_shape[0] - self.pad_top
        self.pad_left = (self.input_shape[1] - img_shape[1])//2
        self.pad_right = self.input_shape[1] - img_shape[1] - self.pad_left
        self.model_neuron = torch.jit.load(f'BSR_x{scale}_neuron.pt')
    def __call__(self, img):
        img = cv2.copyMakeBorder(img, self.pad_top, self.pad_bottom, self.pad_left, self.pad_right, cv2.BORDER_REFLECT)
        y = np.zeros((self.input_shape[0]*2, self.input_shape[1]*2, 3)).astype('uint16')
        weight = np.zeros((self.input_shape[0]*2, self.input_shape[1]*2, 3)).astype('uint16')
        for patch in self.patches:
            input_frame = np.expand_dims((np.transpose(img[patch[0], patch[1],...], (2, 0, 1)))/255, 0).astype('float32')
            rlt = self.model_neuron(torch.from_numpy(input_frame))
            rlt = utils.tensor2img(rlt)
            y[slice(patch[0].start * 2, patch[0].stop * 2), slice(patch[1].start * 2, patch[1].stop * 2),...] += rlt
            weight[slice(patch[0].start * 2, patch[0].stop * 2), slice(patch[1].start * 2, patch[1].stop * 2),...] += 1
        y = y / weight
        y = y[self.pad_top*2:y.shape[0]-self.pad_bottom*2,
              self.pad_left*2:y.shape[1]-self.pad_right*2]
        return y
    
model = GANInference(img_shape, scale)


probe_output = None
if os.path.exists(os.path.join('/input', fname + '_' + method + ext)):
    output_file = os.path.join('/input', fname + '_' + method + ext)
    try:
        probe_output = ffmpeg.probe(output_file, loglevel = 56)
    except:
        pass
    if not probe_output is None:
        video_stream_output = next((stream for stream in probe_output['streams'] if stream['codec_type'] == 'video'), None)
        width_output = int(video_stream_output['width'])
        height_output = int(video_stream_output['height'])
        if 'duration' in video_stream_output:
            max_len_output =  int(float(video_stream_output['duration']) * round(Fraction(video_stream_output['avg_frame_rate'])))
            if max_len==max_len_output and width_output==width*scale and height_output==height*scale:
                exit()
process = (
    ffmpeg
    .input(video_file, loglevel="quiet", r=avg_frame_rate)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24', r=avg_frame_rate)
    .run_async(pipe_stdout=True)
)

if audio_enable:
    process_w = (
        ffmpeg
        .input('pipe:', format='rawvideo', loglevel="quiet", pix_fmt='rgb24', s='{}x{}'.format(width*scale, height*scale), r=avg_frame_rate)
        .output(audio, os.path.join('/input', fname + '_' + method + ext), pix_fmt='yuv420p', vcodec='libx264', r=avg_frame_rate, crf=19)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )
else:
    process_w = (
        ffmpeg
        .input('pipe:', format='rawvideo', loglevel=0, pix_fmt='rgb24', s='{}x{}'.format(width*scale, height*scale), r=avg_frame_rate)
        .output(os.path.join('/input/', fname + '_' + method + ext), pix_fmt='yuv420p', vcodec='libx264', r=avg_frame_rate, crf=19)
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )

last_percent = -1
for idx in range(max_len):
    try:
        in_bytes = process.stdout.read(width * height * 3)
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )
        rlt = model(in_frame)
        process_w.stdin.write(
            rlt.tobytes()
        )
        percent = round((idx/max_len)*100)
        if percent % 5 ==0 and percent!= last_percent:
            logging.info(f'Processed  {percent}% ...')
            last_percent = percent
    except Exception as e:
        logging.error(e.stderr.decode('utf8') + 'at' + str(idx))
        raise e
        
process_w.stdin.close()
process_w.wait()
os.remove(video_file)
print(video_file + ' finished..')