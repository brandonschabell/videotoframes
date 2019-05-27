import argparse
import base64
import os
from tqdm import tqdm

from videotoframes import convert


def video_to_frames(input_path, output_dir, max_frames, even):
    base_filename = input_path.split(os.path.sep)[-1].split('.')[0]

    with open(input_path, 'rb') as file:
        video_base_64 = base64.b64encode(file.read())

    frames = convert(video_base_64=video_base_64, frame_rate=None, max_frames=max_frames, even=even, return_dict=True)
    for frame in frames:
        base_64_image = frame['base64image']
        frame_number = frame['frameNumber']
        output_path = os.path.join(output_dir, base_filename + '-frame{:03d}.jpg'.format(frame_number))
        with open(output_path, 'wb') as file:
            file.write(base_64_image)

    return True


def main(args=None):
    parser = argparse.ArgumentParser(prog='videotoframes')
    parser.add_argument('-o', required=True, help='output directory')
    parser.add_argument('-i', required=True, nargs='+', help='input video(s).')
    parser.add_argument('--max-frames', type=int, help='optionally include a maximum number of frames into which the '
                                                       'video will be broken.')
    parser.add_argument('--even', action='store_true', help='If a "--max-frames" value is used, this will sample '
                                                            'frames from a uniform distribution as opposed to using '
                                                            'sequential frames.')
    args = parser.parse_args(args)
    output_dir = args.o

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    inp = args.i
    if os.path.isdir(inp[0]):
        inp = [os.path.join(inp[0], f) for f in os.listdir(inp[0]) if os.path.isfile(os.path.join(inp[0], f))]

    if len(inp) == 0:
        raise Exception('No video selected.')

    max_frames = args.max_frames
    even = args.even

    for filename in tqdm(inp, desc='Breaking videos into frames'):
        video_to_frames(filename, output_dir, max_frames, even)
