import os
import cv2
import sys
from tqdm import tqdm


def video_to_frames(input_path, output_dir):
    if input_path is None:
        return None
    video = cv2.VideoCapture(input_path)

    count = 0

    base_filename = input_path.split(os.path.sep)[-1].split('.')[0]

    while True:
        ret, frame = video.read()
        if frame is None:
            break
        count += 1
        output_path = os.path.join(output_dir, base_filename + '-frame{:03d}.jpg'.format(count))
        cv2.imwrite(output_path, frame)

    video.release()
    return True


def main():
    arguments = sys.argv
    arguments.pop(0)

    if len(arguments) == 0:
        return 'No output path specified.'
    output_dir = arguments.pop(0)

    if len(arguments) == 0:
        return 'No video selected.'

    for filename in tqdm(arguments, desc='Breaking videos into frames'):
        video_to_frames(filename, output_dir)
