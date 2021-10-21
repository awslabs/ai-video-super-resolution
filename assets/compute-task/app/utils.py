import ffmpeg
import numpy as np

def get_nb_frames(video_file, width, height, avg_frame_rate):
    process = (
        ffmpeg
        .input(video_file, loglevel="quiet", r=avg_frame_rate)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', r=avg_frame_rate)
        .run_async(pipe_stdout=True)
    )
    max_len = 0
    while True:
        in_bytes = process.stdout.read(width * height * 3)
        b = np.frombuffer(in_bytes, np.uint8)
        if len(b) == 0:
            break
        max_len += 1
    return max_len

def tensor2img(tensor, out_type=np.uint8, min_max=(0, 1)):
    tensor = tensor.squeeze().clamp_(*min_max)  # clamp
    tensor = (tensor - min_max[0]) / (min_max[1] - min_max[0])  # to range [0,1]
    img_np = tensor.numpy()
    img_np = np.transpose(img_np[:, :, :], (1, 2, 0))
    img_np = (img_np * 255.0).round()
    return img_np.astype(out_type)