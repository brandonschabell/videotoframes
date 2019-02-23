import argparse
import os
import cv2
from tqdm import tqdm


def get_frames_to_grab(frame_count, max_frames):
	span = (frame_count -1) / (max_frames - 1)
	return [round(i * span) for i in range(max_frames)]


def video_to_frames(input_path, output_dir, max_frames, even):
	video = cv2.VideoCapture(input_path)

	count = 0

	base_filename = input_path.split(os.path.sep)[-1].split('.')[0]

	frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	if max_frames is None:
		max_frames = frame_count

	if even:
		grab_frames = get_frames_to_grab(frame_count=frame_count, max_frames=max_frames)

		for frame_num in grab_frames:
			video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
			ret, frame = video.read()
			if frame is not None:
				output_path = os.path.join(output_dir, base_filename + '-frame{:03d}.jpg'.format(frame_num))
				cv2.imwrite(output_path, frame)
	else:
		while count < max_frames:
			ret, frame = video.read()
			if frame is not None:
				output_path = os.path.join(output_dir, base_filename + '-frame{:03d}.jpg'.format(count))
				count += 1
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
