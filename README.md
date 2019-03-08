# VideoToFrames

[![PyPI version](https://badge.fury.io/py/videotoframes.svg)](https://badge.fury.io/py/videotoframes)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/videotoframes.svg)](https://pypi.python.org/pypi/videotoframes/)
[![Build Status](https://travis-ci.com/brandonschabell/videotoframes.svg?branch=master)](https://travis-ci.com/brandonschabell/videotoframes)
[![codecov](https://codecov.io/gh/brandonschabell/videotoframes/branch/master/graph/badge.svg)](https://codecov.io/gh/brandonschabell/videotoframes)

A simple Python script to break videos into frames. This package does 
**_NOT_ require ffmpeg**.

## Installation
VideoToFrames requires Python 3.4+

```bash
pip install videotoframes
```

## Example Usage:
VideoToFrames can be run from any command prompt or imported into a Python 
project.

Assuming there is a video at `./videos/example.mp4` and you want to create 
frames in `./frames`:

```bash
videotoframes -i ./vidoes/example.mp4 -o ./frames
```

If you want to create a limited number of frames that are evenly distributed:

```bash
videotoframes -i ./videos/example.mp4 -o ./frames --max-frames=20 --even
```

You can also use VideoToFrames with many videos at once:

```bash
videotoframes -i ./videos -o ./frames
```

Using VideoToFrames in a Python project:
```python
from videotoframes import convert

video_base_64 = '...'
frames = convert(video_base_64=video_base_64, max_frames=10, frame_rate=1)
```

## GitHub Project
https://github.com/brandonschabell/videotoframes

## PyPi Project
https://pypi.org/project/videotoframes/

### Contact

Please feel free to email me at brandonschabell@gmail.com with any questions or feedback.