import argparse
import os
import cv2
from tqdm import tqdm


def video_to_frames(input_path, output_dir, max_frames, even):
    if input_path is None:
        return None
    video = cv2.VideoCapture(input_path)

    count = 0

    base_filename = input_path.split(os.path.sep)[-1].split('.')[0]

    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if max_frames is None:
        max_frames = frame_count

    if even:
        if frame_count % max_frames == 0:
            span = frame_count // max_frames
        else:
            span = frame_count // (max_frames - 1)

        grab_frames = [i for i in range(0, frame_count, span)]

        for frame_num in grab_frames:
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = video.read()
            if frame is None:
                break
            output_path = os.path.join(output_dir, base_filename + '-frame{:03d}.jpg'.format(frame_num))
            cv2.imwrite(output_path, frame)
    else:
        while count < max_frames:
            ret, frame = video.read()
            if frame is None:
                break
            count += 1
            output_path = os.path.join(output_dir, base_filename + '-frame{:03d}.jpg'.format(count))
            cv2.imwrite(output_path, frame)

    video.release()
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

    if len(output_dir) == 0:
        return 'No output path specified.'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    inp = args.i
    if len(inp) == 0:
        return 'No video selected.'
    if os.path.isdir(inp[0]):
        inp = [os.path.join(inp[0], f) for f in os.listdir(inp[0])]

    max_frames = args.max_frames
    even = args.even

    for filename in tqdm(inp, desc='Breaking videos into frames'):
        video_to_frames(filename, output_dir, max_frames, even)
