from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


test_requirements = [
    'pytest'
]

setup(
    name='videotoframes',
    version='1.1.0',
    packages=find_packages(),
    url='https://github.com/brandonschabell/videotoframes',
    download_url='https://github.com/brandonschabell/videotoframes/archive/v1.1.0.tar.gz',
    license='MIT',
    author='Brandon Schabell',
    author_email='brandonschabell@gmail.com',
    description='A simple Python script to break videos into frames.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Utilities'
    ],
    python_requires='~=3.4',
    install_requires=[
        'opencv-python',
        'tqdm'
    ],
    tests_require=test_requirements,
    setup_requires=[
        'pytest-runner'
    ],
    extras_require={
      'tests': test_requirements
    },
    entry_points={
      'console_scripts': ['videotoframes=videotoframes.video_to_frames:main']
    }
)
