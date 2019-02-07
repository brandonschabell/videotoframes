from setuptools import setup, find_packages

setup(
    name='videotoframes',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='Brandon Schabell',
    author_email='brandonschabell@gmail.com',
    description='',
    install_requires=[
        'opencv-python',
        'tqdm'
    ],
    entry_points={
      'console_scripts': ['videotoframes=videotoframes.video_to_frames:main']
    }
)
