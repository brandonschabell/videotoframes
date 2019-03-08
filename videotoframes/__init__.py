import base64
import cv2
from tempfile import NamedTemporaryFile

from videotoframes.video_to_frames import get_frames_to_grab


def convert(video_base_64, frame_rate=None, max_frames=None, even=False):
	with NamedTemporaryFile('wb') as video_file:
		video_file.write(base64.b64decode(video_base_64))
		video = cv2.VideoCapture(video_file.name)

		count = 0

		frames = []

		frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
		if max_frames is None:
			max_frames = frame_count

		if even:
			grab_frames = get_frames_to_grab(frame_count=frame_count, max_frames=max_frames)

			for frame_num in grab_frames:
				video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
				ret, frame = video.read()
				ret, buffer = cv2.imencode('.jpg', frame)
				frames.append(base64.b64encode(buffer))
		elif frame_rate is not None:
			fps = video.get(cv2.CAP_PROP_FPS)
			if frame_rate > fps:
				frame_rate = fps
			time_stamp = 0
			while count < max_frames:
				video.set(cv2.CAP_PROP_POS_MSEC, round(time_stamp))
				ret, frame = video.read()
				if frame is not None:
					count += 1
					ret, buffer = cv2.imencode('.jpg', frame)
					frames.append(base64.b64encode(buffer))
				else:
					break
				time_stamp += 1000 / frame_rate
		else:
			while count < max_frames:
				ret, frame = video.read()
				if frame is not None:
					count += 1
					ret, buffer = cv2.imencode('.jpg', frame)
					frames.append(base64.b64encode(buffer))

		video.release()
		return frames
