import base64
import os

from videotoframes import convert

from tests.utilities import get_testfiles_path


def test_convert():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64)
	assert len(frames) == 166


def test_convert_max_frames():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=10)
	assert len(frames) == 10


def test_main_max_frames_even():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=10, even=True)
	assert len(frames) == 10


def test_convert_max_frames_even_2_frames(tmpdir):
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=2, even=True)
	assert len(frames) == 2
