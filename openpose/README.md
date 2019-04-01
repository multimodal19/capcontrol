# overlay

A C++ implementation of a camera preview window with a parallel thread running
OpenPose and processing as many of the frames as it can.

## Build Requirements
- Visual Studio 2017 (Tested with version 15.9.10, but other versions should
  be fine too)
    - C++ Desktop development component
- [OpenPose C++ API](https://github.com/CMU-Perceptual-Computing-Lab/openpose)


## Installation
1. Build OpenPose. Please refer to the [installation guide](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md#openpose---installation).
2. In the files `camera_pose.vcxproj` & `camera_pose.vcxproj.user` from the
  `OpenPose` subfolder, replace all occurrences of
  `D:\Documents\GitHub\openpose` with your own OpenPose installation path.
3. Open and build solution with Visual Studio.

## Usage
Either just run the application directly from Visual Studio or from the build
directory.

The following interaction is possible:
| Key              | Action                       |
|------------------|------------------------------|
| <kbd>Esc</kbd>   | Quit the application         |
| <kbd>Space</kbd> | Toggle show processed frames |
| <kbd>f</kbd>     | Toggle FPS indicator         |
| <kbd>m</kbd>     | Toggle mirroring             |
