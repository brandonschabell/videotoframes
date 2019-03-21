import base64
import os
import warnings

from videotoframes import convert

from tests.utilities import get_testfiles_path


def test_convert():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64)
	assert frames[0] != frames[-1]
	assert len(frames) == 166


def test_convert_max_frames():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=10)
	assert frames[0] != frames[-1]
	assert len(frames) == 10


def test_main_max_frames_even():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=10, even=True)
	assert frames[0] != frames[-1]
	assert len(frames) == 10


def test_convert_max_frames_even_2_frames():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=2, even=True)
	assert frames[0] != frames[-1]
	assert len(frames) == 2


def test_convert_frame_rate():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, frame_rate=2)
	assert frames[0] != frames[-1]
	assert len(frames) == 12


def test_convert_frame_rate_small():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, frame_rate=1)
	assert frames[0] != frames[-1]
	assert len(frames) == 6


def test_convert_frame_rate_divisible():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, frame_rate=15)
	assert frames[0] != frames[-1]
	assert len(frames) == 83


def test_convert_frame_rate_full():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, frame_rate=30)
	assert frames[0] != frames[-1]
	assert len(frames) == 166


def test_convert_frame_rate_higher_than_full():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, frame_rate=40)
	assert frames[0] != frames[-1]
	assert len(frames) == 166


def test_convert_frame_rate_max_frames():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=8, frame_rate=2)
	assert len(frames) == 8
	assert frames[0] != frames[-1]


def test_convert_frame_rate_max_frames_higher_than_frame_count():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=13, frame_rate=2)
	assert len(frames) == 12
	assert frames[0] != frames[-1]


def test_convert_deprecate_list_response():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()


	with warnings.catch_warnings(record=True) as w:
		# Cause all warnings to always be triggered.
		warnings.simplefilter("always")
		convert(video_base_64, max_frames=13, frame_rate=2)

		assert len(w) == 1
		assert issubclass(w[-1].category, DeprecationWarning)
		assert "Returning a list instead of a list of dictionaries." in str(w[-1].message)


def test_convert_dictionary_return():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=5, frame_rate=1, return_dict=True)
	assert len(frames) == 5
	for frame in frames:
		assert isinstance(frame, dict)
		assert set(frame.keys()) == {'base64image'}
	assert frames[0] != frames[-1]


def test_convert_video_timestamp():
	with open(os.path.join(get_testfiles_path(), 'small.mp4'), 'rb') as file:
		video_base_64 = base64.b64encode(file.read()).decode()
	frames = convert(video_base_64, max_frames=6, frame_rate=4, video_timestamp='2019-02-10 20:25:00')
	assert len(frames) == 6
	for frame in frames:
		assert isinstance(frame, dict)
		assert set(frame.keys()) == {'base64image', 'timestamp'}
	assert ['2019-02-10 20:25:00',
			'2019-02-10 20:25:00',
			'2019-02-10 20:25:00',
			'2019-02-10 20:25:00',
			'2019-02-10 20:25:00',
			'2019-02-10 20:25:00'] == [frame['timestamp'] for frame in frames]
