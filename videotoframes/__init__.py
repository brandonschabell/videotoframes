import base64
import cv2
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile
import warnings

DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_frames_to_grab(frame_count, max_frames):
    span = (frame_count - 1) / (max_frames - 1)
    return [round(i * span) for i in range(max_frames)]


def convert(video_base_64, frame_rate=None, max_frames=None, even=False, video_timestamp=None, return_dict=False):
    if video_timestamp is not None and not return_dict:
        warnings.warn('Ignoring return_dict=False since a video_timestamp has been specified.')
        return_dict = True
    if not return_dict:
        warnings.warn(
            'Returning a list instead of a list of dictionaries. This option will be removed in a future release when '
            'all frames will be returned in dictionaries.',
            DeprecationWarning)

    if video_timestamp is not None:
        video_timestamp = datetime.strptime(video_timestamp, DATE_TIME_FORMAT)

    with NamedTemporaryFile('wb') as video_file:
        video_file.write(base64.b64decode(video_base_64))
        video = cv2.VideoCapture(video_file.name)

        count = 0

        frames = []

        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)
        _, frame = video.read()
        if frame is None:
            frame_count -= 1
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if max_frames is None:
            max_frames = frame_count

        if even:
            grab_frames = get_frames_to_grab(frame_count=frame_count, max_frames=max_frames)

            for frame_number in grab_frames:
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                _, frame = video.read()
                if frame is not None:
                    _, buffer = cv2.imencode('.jpg', frame)
                    return_frame = get_return_frame(buffer, return_dict, video, video_timestamp, frame_number)
                    frames.append(return_frame)
                else:
                    break
        elif frame_rate is not None:
            fps = video.get(cv2.CAP_PROP_FPS)
            if frame_rate > fps:
                frame_rate = fps
            time_stamp = 0
            max_timestamp = frame_count * 1000 / fps
            while count < max_frames and time_stamp <= max_timestamp:
                video.set(cv2.CAP_PROP_POS_MSEC, round(time_stamp))
                _, frame = video.read()
                if frame is not None:
                    _, buffer = cv2.imencode('.jpg', frame)
                    return_frame = get_return_frame(buffer, return_dict, video, video_timestamp, count)
                    frames.append(return_frame)
                    count += 1
                else:
                    break
                time_stamp += 1000 / frame_rate
        else:
            while count < max_frames:
                _, frame = video.read()
                if frame is not None:
                    _, buffer = cv2.imencode('.jpg', frame)
                    return_frame = get_return_frame(buffer, return_dict, video, video_timestamp, count)
                    frames.append(return_frame)
                    count += 1
                else:
                    break

        video.release()
        return frames


def get_return_frame(buffer, return_dict, video, video_timestamp, frame_number):
    return_frame = base64.b64encode(buffer)
    if return_dict:
        return_frame = {
            'base64image': return_frame,
            'frameNumber': frame_number
        }
        if video_timestamp is not None:
            frame_offset_ms = video.get(cv2.CAP_PROP_POS_MSEC)
            frame_datetime = video_timestamp + timedelta(milliseconds=frame_offset_ms)
            return_frame['timestamp'] = frame_datetime.strftime(DATE_TIME_FORMAT)
    return return_frame
